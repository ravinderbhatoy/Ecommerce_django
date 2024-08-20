from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.user_register, name='register'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('add-cart', views.add_cart, name='add-cart'),
    path('delete-cart', views.delete_cart, name='delete-cart'),
    path('update-cart/<int:product_id>', views.update_cart, name='update-cart'),
    path('cart', views.user_cart, name='user-cart'),
    path('shop', views.shop, name='shop'),
    path('product-detail/<int:id>', views.product_detail, name='product-detail'),
    path('contact', views.contact, name='contact'),
    path('add-review', views.add_review, name='add-review'),
    path('delete-review/<int:product_id>', views.delete_review, name='delete-review'),
    path('mail-sender', views.mail_sender, name='mail-sender'),
    path('checkout', views.checkout, name='checkout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)