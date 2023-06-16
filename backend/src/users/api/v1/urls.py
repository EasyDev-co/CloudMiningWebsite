from django.urls import path, include, re_path
from src.users.api.v1.views import (
    UserRegistrationView,
    UserActivationAccountView,
    ResendActivationAccountEmailView,
    UserLoginView
)
from django.contrib.auth import get_user_model
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    # path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # re_path(r'^auth/', include('djoser.urls.jwt'))
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('activation/<token>/', UserActivationAccountView.as_view(), name='activation'),
    path('activation/resend/<email>', ResendActivationAccountEmailView.as_view(), name='resend_activation'),
    path('login/', UserLoginView.as_view(), name='login')
]
