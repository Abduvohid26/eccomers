from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, NotFound
from products.serializers import ProductSerializer, CartSerializer
from shared.uitility import send_phone_numer
from .models import User


class SignUpSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    auth_status = serializers.CharField(read_only=True, required=False)
    password_confirmation = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'auth_status',
            'username',
            'phone_number',
            'password',
            'password_confirmation',


        )

    def create(self, validated_data):
        user = super(SignUpSerializer, self).create(validated_data)
        print('user', user)
        code = user.create_verify_code()
        send_phone_numer(user.phone_number, code)
        user.save()
        return user

    def validate(self, data):
        username = data.get('username').lower()
        password = data.get('password')
        password_confirmation = data.get('password_confirmation')
        phone_number = data.get('phone_number').lower()

        if username and User.objects.filter(username=username).exists():
            raise ValidationError({'success': False, 'message': 'Username already exists'})

        if password != password_confirmation:
            raise ValidationError({'success': False, 'message': 'Passwords do not match'})

        if phone_number and User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError({'success': False, 'message': 'Phone number already exists'})

        return data

    def phone_validate(self, value):
        value = self.lower()
        if value and User.objects.filer(phone_number=value).exists():
            data = {
                'success': False,
                'message': ' phono number already exists.'
            }
            return ValidationError(data)
        return value

    def to_representation(self, instance):
        print('to_representation', instance)
        data = super(SignUpSerializer, self).to_representation(instance)
        data.update(instance.token())
        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'phone_number', 'user_roles')


class LoginSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']


class ForgetPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        phone_number = data.get('phone_number', None)
        if phone_number is None:
            raise ValidationError(
                {
                    'success': False,
                    'message': 'Invalid phone number'
                }
            )
        user = User.objects.filter(phone_number=phone_number)
        if not user.exists():
            raise NotFound(detail='User not found')
        data['user'] = user.first()
        return data


class ResetPasswordSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    password = serializers.CharField(write_only=True, required=True)
    password_confirmation = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'id',
            'password',
            'password_confirmation'
        ]

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirmation = attrs.get('password_confirmation')
        if password != password_confirmation:
            raise ValidationError({'success': False, 'message': 'Passwords do not match'})
        return attrs

    def update(self, instance, validated_data):
        password = validated_data.pop('password')
        instance.set_password(password)
        return super(ResetPasswordSerializer, self).update(instance, validated_data)
