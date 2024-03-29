from django.urls import path
from .views import (SignUpView, CodeVerifiedView, GetNewVerifyCodeView, UsersAPIView, UserAPIView, LoginAPIView,
                    ForgetPasswordView, ResetPasswordView)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('verify/', CodeVerifiedView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('new-verify/', GetNewVerifyCodeView.as_view()),
    path('forget-password/', ForgetPasswordView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),
    path('api/', UsersAPIView.as_view()),
    path('api/<uuid:id>', UserAPIView.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view())
]


