from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Product, Cart, Comment, cartItem
from django.http import JsonResponse
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator

import json

# home page
def home(request):
    products = Product.objects.all()[:8]
    vegetables = Product.objects.filter(category="vegetables")
    fruits = Product.objects.filter(category="fruits")
    context = {'all_products': products, 'vegetables': vegetables, 'fruits': fruits}
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        cart_items = cartItem.objects.filter(cart=cart)
        if cart is not None:
            context['cart_count'] = cart_items.all().count()
    return render(request, 'shop/index.html', context=context)
# handling reviews
def add_review(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                data = json.loads(request.body)
                product = Product.objects.get(id=data['product_id'])
                user = request.user
                # comment = Comment.objects.create(user=user, product=product, review=review)
                comment, created = Comment.objects.get_or_create(user=user, product=product)
                if not created:
                    print("Comment already exists")
                    return JsonResponse({'status': 'user comment already exists'}, status=400)
                else:
                    comment.review = data['review']
                    comment.save()
                    print("Comment added successfully")
                    return JsonResponse({'status': 'success'})
            except:
                print("Failed to add comment")
                return JsonResponse({'status': 'failed'})
        else:
            return redirect('login')

def delete_review(request, product_id):
    if request.method == "POST":
        print('Deleting review...')
        if request.user.is_authenticated:
            try:
                user = request.user
                product = Product.objects.get(id=product_id)
                comment = Comment.objects.get(user=user, product=product)
                comment.delete()
                return JsonResponse({"status": 'success'}) 
            except:
                return JsonResponse({'status': 'failed'})
    return redirect('product-detail', product_id)

# handling shop
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    context = {'product': product}
    if request.user.is_authenticated:
        if product.category == 'vegetables':
            related_products = Product.objects.filter(category="vegetables")
            context['related_products'] = related_products
        else:
            related_products = Product.objects.filter(category="fruits")
            context['related_products'] = related_products
        cart = Cart.objects.get(user=request.user)
        cart_items = cartItem.objects.filter(cart=cart).count()
        context['cart_count'] = cart_items 
    return render(request,'shop/product-detail.html', context=context)

def shop(request):
    context = {}
    prices = ['1', '2', '3', '4', '5', '6','7', '8', '9', '10']
    search_post = request.GET.get('search')
    sort_product = request.GET.get('sort')
    if sort_product:
        products_list = []
        if sort_product == 'low-to-high':
            products = Product.objects.all().order_by('price')
        elif sort_product == 'high-to-low':
            products = Product.objects.all().order_by('-price')
        elif sort_product in prices:
            products = Product.objects.filter(price__lte=sort_product)
        for product in products:
           products_list.append({
                'id': product.id,
                'title': product.title,
                'description': product.description,
                'price': product.price,
                'category': product.category,
                'image_url': request.build_absolute_uri(product.image.url) 
           }) 
        return JsonResponse({'products':products_list})
    if search_post:
        products = Product.objects.filter(Q(title__icontains=search_post) | Q(description__icontains=search_post))
    else:
        products = Product.objects.all()
    fruite_count = Product.objects.filter(category='fruits').count()
    vegetable_count = Product.objects.filter(category='vegetables').count()
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'products': page_obj, 'fruite_count': fruite_count, 'vegetable_count': vegetable_count}
    if request.user.is_authenticated:
        cart,created = Cart.objects.get_or_create(user=request.user)
        cart_items = cartItem.objects.filter(cart=cart).all()
        context['cart_count'] = cart_items.count()
    return render(request, 'shop/shop.html', context=context)
# handling cart

def user_cart(request):
    if request.user.is_authenticated:
        cart,created = Cart.objects.get_or_create(user=request.user)
        cart_items = cartItem.objects.filter(cart=cart)
        context = {'cart': cart_items, 'cart_count':cart_items.all().count()}
        return render(request, 'shop/cart.html', context=context)
    else:
        return redirect('login')

def delete_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('productId')
        print(product_id)
        if product_id is not None:
            print("product_id is not None")
            product = get_object_or_404(Product, pk=product_id)
            cart,created = Cart.objects.get_or_create(user=request.user)
            cart_item = cartItem.objects.filter(cart=cart, product=product).first()
            if cart_item:
                cart_item.delete()
            print("Deleted succesfully")
            return JsonResponse({"message": "Product removed from cart successfully"})
    return JsonResponse({"error": "Invalid request method"}, status=405)


def update_cart(request, product_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        quantity = data.get('quantity')
        if quantity is None:
            return JsonResponse({'success': False,'message': 'Quantity not provided'}, status=400)
        user = request.user
        product = Product.objects.get(id=product_id)
        user_cart, created = Cart.objects.get_or_create(user=user)
        cart_item, created = cartItem.objects.get_or_create(cart=user_cart, product=product)
        print(f"Changing cart value of {cart_item.product.title} to {quantity}")
        cart_item.quantity = quantity 
        cart_item.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


def add_cart(request):
    if request.method == "POST":
        if request.user.is_authenticated:
        # Parse the JSON data from the request body
            data = json.loads(request.body)
            product_id = data.get('product_id')
            if product_id is not None:
                product = get_object_or_404(Product, pk=product_id)
                print(product)
                # Process further logic (e.g., add to cart)
                cart,created = Cart.objects.get_or_create(user=request.user)
                cart_item, created= cartItem.objects.get_or_create(cart=cart, product=product)
                cart_total = cartItem.objects.filter(cart=cart).all().count()
                cart_item.quantity+=1
                cart_item.save()
                print("Product added to cart successfully")
                return JsonResponse({'message': 'Product added to cart successfully', 'cart_count':cart_total})
            else:
                # Handle case where product_id is not provided
                return JsonResponse({'error': 'Product ID not provided'}, status=400)
        else:
            return JsonResponse({"error": "User not authenticated"}, status=401)
        # Handle other HTTP methods if needed
    return JsonResponse({'error': 'Invalid request method'}, status=405)

# handling user
def user_register(request):
    print("Making registration request....")
    message = ""
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirmPassword']
        is_exist = User.objects.filter(email=email).exists()
        if is_exist:
            message = 'Email already exists!'
            return render(request, 'shop/register.html', context={'message': message})
        if password == confirm_password:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                print(request.user)
                return redirect('home')
            else:
                message = "An error occured!"
        else:
            message = "Password doesn't matched"
    return render(request, 'shop/register.html', context={'message': message})

def user_login(request):
    # logout(request)
    message = ""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            message = "invalid details"
    return render(request, 'shop/login.html', context={'message': message})

def user_logout(request):
    logout(request)
    return redirect('home')

# contact page
def contact(request):
    if request.method == 'POST':
        print("sending email....")
        user_email = request.POST['email']
        name = request.POST['name']
        message = request.POST['message']
        print(user_email)
        if user_email:
            sender = settings.EMAIL_HOST_USER
            print("Sender", sender)
            try:
                send_mail(
                    subject="Get in touch",
                    message=f"from {user_email}\n{message}",
                    from_email=sender,
                    recipient_list=[sender],
                    fail_silently=False,
                )
                print("Email sent successfully")
            except Exception as e:
                print(e)
        else:
            print("Error in sending email")
    return render(request, 'shop/contact.html')

# sending email
def mail_sender(request):
    if request.method == 'POST':
        print("sending email....")
        user_email = request.POST['email']
        print(user_email)
        if user_email:
            sender = settings.EMAIL_HOST_USER
            print("Sender", sender)
            try:
                send_mail(
                    subject="Welcome email",
                    message="Thanks for joining us",
                    from_email=sender,
                    recipient_list=[user_email],
                    fail_silently=False,
                )
                print("Email sent successfully")
            except Exception as e:
                print(e)
        else:
            print("Error in sending email")
    return redirect(request.META.get('HTTP_REFERER', '/'))

# checkout page
def checkout(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        cart_item = cartItem.objects.filter(cart=cart)
        context = {'cart': cart_item, 'cart_count': cart_item.all().count()}
    return render(request, 'shop/checkout.html', context=context)
