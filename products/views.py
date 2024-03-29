from django.shortcuts import render
from rest_framework import permissions, status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, Category, Comment, Cart, Order
from .serializers import ProductSerializer, CategorySerializer, CommentSerializer, CartSerializer, OrderSerializer


class ProductAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        categories = Product.objects.all()
        serializer = ProductSerializer(categories, many=True)
        return Response(data=serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=id)
        serializer = ProductSerializer(product)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=id)
        product_serializer = ProductSerializer(instance=product, data=request.data)
        if product_serializer.is_valid():
            product_serializer.save()
            return Response(data=product_serializer.data, status=status.HTTP_200_OK)
        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=id)
        product_serializer = ProductSerializer(instance=product, data=request.data)
        if product_serializer.is_valid():
            product_serializer.save()
            return Response(data=product_serializer.data, status=status.HTTP_200_OK)
        return Response(data=product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=id)
        product.delete()
        return Response(data={'message': 'Product successfully deleted!'}, status=status.HTTP_200_OK)


class CategoryAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(data=serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        category = get_object_or_404(Category, id=id)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id, *args, **kwargs):
        category = get_object_or_404(Category, id=id)
        serializer = CategorySerializer(instance=category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        category = get_object_or_404(Category, id=id)
        serializer = CategorySerializer(instance=category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        category = get_object_or_404(Category, id=id)
        category.delete()
        return Response(data={'message': 'Category successfully deleted!'}, status=status.HTTP_200_OK)


class CommentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(data=serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, id=id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, id=id)
        serializer = CommentSerializer(instance=comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, id=id)
        serializer = CommentSerializer(instance=comment, data=request)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, id=id)
        comment.delete()
        return Response(data={'message': 'comment successfully deleted!'}, status=status.HTTP_200_OK)


class CartAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        cart = Cart.objects.all()
        serializer = CartSerializer(cart, many=True)
        return Response(data=serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, id=id)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, id=id)
        serializer = CartSerializer(instance=cart, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, id=id)
        serializer = CartSerializer(instance=cart, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, id=id)
        cart.delete()
        return Response(data={'message': 'Deleted successfully'}, status=status.HTTP_200_OK)


class OrderAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        order = Order.objects.all()
        serializer = OrderSerializer(order, many=True)
        return Response(data=serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=id)
        serializer = OrderSerializer(order)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        order = get_object_or_404(Order,id=id)
        serializer = OrderSerializer(instance=order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=id)
        serializer = OrderSerializer(instance=order, data=request)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=id)
        order.delete()
        return Response(data={'message': 'Deleted successfully'}, status=status.HTTP_200_OK)