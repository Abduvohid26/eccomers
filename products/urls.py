from .views import ProductAPIView, CategoryAPIView, CommentAPIView, CartAPIView, OrderAPIView, ProductDetailAPIView, \
    CartDetailAPIView, CategoryDetailAPIView, CommentDetailAPIView, OrderDetailAPIView
from django.urls import path
urlpatterns = [
    path('api', ProductAPIView.as_view()),
    path('api/<uuid:id>', ProductDetailAPIView.as_view()),
    path('api/categories', CategoryAPIView.as_view()),
    path('api/categories/<uuid:id>', CategoryDetailAPIView.as_view()),
    path('api/comments', CommentAPIView.as_view()),
    path('api/comments/<uuid:id>', CommentDetailAPIView.as_view()),
    path('api/cart', CartAPIView.as_view()),
    path('api/cart/<uuid:id>', CartDetailAPIView.as_view()),
    path('api/order', OrderAPIView.as_view()),
    path('api/order/<uuid:id>', OrderDetailAPIView.as_view())
]
