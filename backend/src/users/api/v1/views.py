from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from src.users.api.v1.serializers import (
    UserRegisterSerializer,
    UserActivationAccountSerializer,
    ResendActivationAccountEmailSerializer,
    LoginUserSerializer,
    SendResetPasswordEmailSerializer,
)
from src.users.tasks import send_email_for_user
from src.users.utils import (
    get_data_for_activation_account_email,
    get_data_for_reset_password_email
)
from src.users.api.v1.renderars import UserDataRender

User = get_user_model()


class UserRegistrationView(generics.GenericAPIView):

    serializer_class = UserRegisterSerializer
    renderer_classes = (UserDataRender,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data.get('email'))
        data = get_data_for_activation_account_email(
            user=user,
            request=request
        )
        send_email_for_user.delay(
            data=data
        )

        return Response(user_data, status=status.HTTP_201_CREATED)


class ResendActivationAccountEmailView(generics.GenericAPIView):
    serializer_class = ResendActivationAccountEmailSerializer
    renderer_classes = (UserDataRender,)

    def get(self, request, email):
        serializer = self.serializer_class(data={'email': email})
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=serializer.data.get('email'))
        data = get_data_for_activation_account_email(
            user=user,
            request=request
        )
        send_email_for_user.delay(
            data=data
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserActivationAccountView(APIView):
    serializer_class = UserActivationAccountSerializer
    renderer_classes = (UserDataRender,)

    def get(self, request, token):
        serializer = self.serializer_class(data={'token': token})
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(pk=serializer.data.get('uuid'))
        user.is_confirm = True
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserLoginView(generics.GenericAPIView):
    serializer_class = LoginUserSerializer
    renderer_classes = (UserDataRender,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = SendResetPasswordEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=serializer.data.get('email'))
        data = get_data_for_reset_password_email(
            user=user,
            request=request
        )
        send_email_for_user.delay(
            data=data
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


class CheckTokenForResetPasswordView(generics.GenericAPIView):
    def get(self, request, uidb64: str, token: str):
        pass