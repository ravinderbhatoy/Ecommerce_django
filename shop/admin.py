from django.contrib import admin
from .models import Product, Cart, Comment, cartItem

# Register your models here.

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Comment)
admin.site.register(cartItem)
