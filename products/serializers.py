import uuid

from rest_framework import serializers

from products.models import Product, Category, Comment, Cart, Order


class ProductSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField()
    class Meta:
        model = Product
        fields = ('id', 'created_at', 'updated_at', 'product_status', 'user', 'title', 'description', 'price', 'month_price',
                  'quantity', 'image', 'slug', 'stars', 'likes', 'discount', 'discount_title',
                  'discount_start_time', 'discount_end_time', 'new_price', 'is_discount_active', 'category')


class CategorySerializer(serializers.ModelSerializer):
    # name = serializers.CharField(source='category__name')

    class Meta:
        model = Category
        fields = ('id', 'name', 'created_at', 'updated_at',)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
