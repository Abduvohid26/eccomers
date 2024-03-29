from django.contrib import admin
from .models import Product, Comment, Cart, Category, Order
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'quantity', 'user', 'product_status')
    search_fields = ('title', 'slug', 'id', 'user',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Comment)
admin.site.register(Cart)
admin.site.register(Category)
admin.site.register(Order)
