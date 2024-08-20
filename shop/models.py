from django.db import models
from django.contrib.auth.models import User

# Create your models here.

choices = (
    ('fruits', 'Fruits'),
    ('vegetables', 'Vegetables'),
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    price = models.FloatField()
    image = models.ImageField(upload_to='images/')
    card_image = models.ImageField(upload_to='images/', null=True)
    category = models.CharField(choices=choices, default='fruits', max_length=10, null=True)
    def __str__(self):
        return self.title

class Cart(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user.username}'s Cart"

class cartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product.title} - {self.quantity}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    review = models.TextField(max_length=500)
    posted_at = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return f"{self.user.username}'s review on {self.product.title}"
