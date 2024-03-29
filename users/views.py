import json
import uuid

from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from products.models import Category, Cart, Product, Order, Comment
from products.serializers import ProductSerializer, CartSerializer, CommentSerializer, CategorySerializer, \
    OrderSerializer
from shared.uitility import send_phone_numer
from .serializers import UserSerializer, LoginSerializer, ForgetPasswordSerializer, ResetPasswordSerializer
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.views import APIView
from django.utils import timezone
from .models import User
from .serializers import SignUpSerializer

class SignUpView(generics.CreateAPIView):
    serializer_class = SignUpSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]


class CodeVerifiedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        code = request.data.get('code')
        self.check_verify(user, code)
        return Response(
            {
                'id': user.id,
                'user': user.username,
                'auth_status': user.user_status,
                'access_token': user.token()['access_token'],
                'refresh_token': user.token()['refresh_token'],

            }
        )

    @staticmethod
    def check_verify(user, code):
        verified = user.verify_codes.filter(code=1111, is_confirmed=False, expiration_time__gte=timezone.now())
        if not verified.exists():
            data = {
                'success': False,
                'message': 'Code error or old'
            }
            raise ValidationError(data)
        else:
            verified.update(is_confirmed=True)
        if user.user_status == NEW:
            user.user_status = CODE_VERIFIED
            user.save()

        return user


class GetNewVerifyCodeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        code = user.create_verify_code()
        self.check_verify_new_code(user)
        if user:
            send_phone_numer(user.phone_number, code)
        else:
            data = {
                'message': 'Kod xato yoki older',
            }
            raise ValidationError(data)
        return Response(
            {
                'success': True,
                'message': 'Verification code returned successfully'
            }
        )

    def check_verify_new_code(self, user):
        verified = user.verify_codes.filter(is_confirmed=False, expiration_time__gte=timezone.now())
        if verified.exists():
            data = {
                'success': False,
                'message': 'Your code valid'
            }
            raise ValidationError(data)


class UserAPIView(APIView):
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        user = User.objects.get(id=str(uuid.UUID(str(id))))
        user_serializer = UserSerializer(user)
        product_serializer = ProductSerializer(user.products.all(), many=True)
        cart_serializer = CartSerializer(user.cart.all(), many=True)
        comment_serializer = CommentSerializer(user.comment.all(), many=True)
        categories = user.products.all().values('category').distinct()
        category_instances = Category.objects.filter(id__in=categories)
        category_serializer = CategorySerializer(category_instances, many=True)

        order_serializer = OrderSerializer(user.order.all(), many=True)
        response_data = {
            'user': user_serializer.data,
            'product': product_serializer.data,
            'cart': cart_serializer.data,
            'comment': comment_serializer.data,
            'category': category_serializer.data,
            'order': order_serializer.data
        }
        return Response(data=response_data, status=status.HTTP_200_OK)

    def put(self, request, id):
        user = get_object_or_404(User, id=str(uuid.UUID(str(id))))
        user_serializer = UserSerializer(instance=user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(data=user_serializer.data, status=status.HTTP_200_OK)
        return Response(data=user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(data=user_serializer.data, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        user = get_object_or_404(User, id=str(uuid.UUID(str(id))))
        user_serializer = UserSerializer(instance=user, data=request.data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(data=user_serializer.data, status=status.HTTP_200_OK)
        return Response(data=user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        user = get_object_or_404(User, id=str(uuid.UUID(str(id))))
        user.delete()
        return Response(data={'message': 'Successfully deleted!'}, status=status.HTTP_200_OK)


class UsersAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        users = User.objects.all()
        response_data = {'users': []}

        for user in users:
            user_data = {}
            user_serializer = UserSerializer(user)
            user_data['user'] = user_serializer.data

            products = Product.objects.filter(user=user)
            product_serializer = ProductSerializer(products, many=True)
            user_data['products'] = product_serializer.data

            carts = Cart.objects.filter(user=user)
            cart_serializer = CartSerializer(carts, many=True)
            user_data['carts'] = cart_serializer.data

            comments = Comment.objects.filter(user=user)
            comment_serializer = CommentSerializer(comments, many=True)
            user_data['comments'] = comment_serializer.data

            categories = Product.objects.filter(user=user).values('category').distinct()
            category_instances = Category.objects.filter(id__in=categories)
            category_serializer = CategorySerializer(category_instances, many=True)
            user_data['categories'] = category_serializer.data

            orders = Order.objects.filter(user=user)
            order_serializer = OrderSerializer(orders, many=True)
            user_data['orders'] = order_serializer.data

            response_data['users'].append(user_data)

        return Response(data=response_data, status=status.HTTP_200_OK)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCartDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]
    cart_id = 'id'
    lookup_field = cart_id

    def get_queryset(self):
        user_id = self.kwargs['id']
        return Cart.objects.filter(user_id=user_id)


class UserProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        user_id = self.kwargs['id']
        product_id = self.kwargs['product_id']
        return Product.objects.filter(user_id=user_id, id=product_id)


class UserCategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    category_id = 'id'
    lookup_field = category_id

    def get_queryset(self):
        user_id = self.kwargs['id']
        return Category.objects.filter(user_id=user_id)


class UserCommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    comment_id = 'id'
    lookup_field = comment_id

    def get_queryset(self):
        user_id = self.kwargs['id']
        return Comment.objects.filter(user_id=user_id)


class UserOrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    order_id = 'id'
    lookup_field = order_id

    def get_queryset(self):
        user_id = self.kwargs['id']
        return Order.objects.filter(user_id=user_id)


class LoginAPIView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            return Response(
                {
                    'id': user.id,
                    'user': user.username,
                    'access_token': user.token()['access_token'],
                    'refresh_token': user.token()['refresh_token'],
                    'status': user.user_status

                }
            )
        else:
            return Response(
                {
                    'success': False,
                    'message': 'Username or password error'

                }, status=status.HTTP_401_UNAUTHORIZED
            )


class ForgetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_classes = ForgetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_classes(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data.get('phone_number')
        user = serializer.validated_data.get('user')
        code = user.create_verify_code()
        send_phone_numer(phone_number, code)
        return Response(
            {
                'success': True,
                'message': 'Verify code successfully send',
                'access': user.token()['access_token'],
                'refresh': user.token()['refresh_token']
            }
        )


class ResetPasswordView(generics.UpdateAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['put', 'patch']

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        response = super(ResetPasswordView, self).update(request, *args, **kwargs)
        try:
            user = User.objects.get(id=response.data.get('id'))
        except ObjectDoesNotExist as e:
            raise NotFound(detail='User not found')

        return Response(
            {
                'success': True,
                'message': 'Password successfully updated',
                'access_token': user.token()['access_token'],
                'refresh_token': user.token()['refresh_token'],
            }
        )