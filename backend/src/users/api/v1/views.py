import os
import requests
from dotenv import load_dotenv
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from src.users.api.v1.serializers import (
    UserRegisterSerializer,
    UserTokenSerializer,
    ResendActivationAccountEmailSerializer,
    LoginUserSerializer,
    SendResetPasswordEmailSerializer,
    CheckNewPasswordSerializer,
    ChangeUserFirstNameSerializer,
    ChangeUserLastNameSerializer,
    ChangeUserPhoneNumberSerializer,
    ChangeUserPasswordSerializer,
    ChangeUserEmailSerializer,
    ChangeUserUsernameSerializer,
    UserTokenUIDSerializer
)
from src.users.tasks import (
    send_email_for_user,
    create_user_wallet
)
from src.users.utils import (
    get_data_for_activation_account_email,
    get_data_for_reset_password_email,
    get_data_for_add_new_email_for_user_email
)
from src.users.api.v1.renderars import UserDataRender
from src.users.models import NewEmail

load_dotenv()

BASE_URL = os.environ.get("BASE_URL")

User = get_user_model()


class GetUserDataView(APIView):
    """
    Возвращает данные авторизированного пользователя
    """
    permission_classes = [IsAuthenticated, ]
    renderer_classes = (UserDataRender,)

    def get(self, request):
        user_data = {
            'uuid': str(request.user.uuid),
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'username': request.user.username,
            'email': request.user.email,
            'phone_number': request.user.phone_number
        }
        return Response(
            data=user_data,
            status=status.HTTP_200_OK
        )


class UserRegistrationView(generics.GenericAPIView):
    """
    Регистрация пользователя.

    После отправки запроса на переданный адрес эл.почты
    придет письмо с ссылкой для активации аккаунта

    Если не активировать, аккаунт, то пользователь не
    сможет залогиниться
    """

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
    """
    Повторная отправка письма для подтверждения аккаунта.
    Запрос на данный эндпоинт может быть отправлен 1 раз в 1 минуту
    """
    serializer_class = ResendActivationAccountEmailSerializer
    renderer_classes = (UserDataRender,)
    throttle_classes = (AnonRateThrottle,)

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
    """
    Обработка ссылки для активации аккаунта.
    """
    serializer_class = UserTokenSerializer
    renderer_classes = (UserDataRender,)

    def get(self, request, token):
        serializer = self.serializer_class(data={'token': token})
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(pk=serializer.data.get('uuid'))
        user.is_confirm = True
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserLoginView(generics.GenericAPIView):
    """
    Авторизация пользователя в системе.

    Вернет refresh и access токены
    """
    serializer_class = LoginUserSerializer
    renderer_classes = (UserDataRender,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        access_token = serializer.data.get('tokens').get('access')
        create_user_wallet.delay(
            access_token=access_token
        )
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ResetPasswordView(generics.GenericAPIView):
    """
    Сброс пароля.
    После отправки запроса с валидным адресом эл.почты,
    на нее будет отправленно письмо с ссылкой на для ввода нового пароля
    """
    serializer_class = SendResetPasswordEmailSerializer
    throttle_classes = (AnonRateThrottle,)
    renderer_classes = (UserDataRender,)

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
    """
    Проверяет переданные данные из ссылки для сброса пароля и
    валидирует новый пароль пользователя
    """
    serializer_class = CheckNewPasswordSerializer
    renderer_classes = (UserDataRender,)

    def put(self, request, **kwargs):
        uidb64 = kwargs.get('uidb64', '')
        token = kwargs.get('token', '')
        uuid_token_serializer = UserTokenUIDSerializer(
            data={
                'uidb64': uidb64,
                'token': token
            }
        )
        uuid_token_serializer.is_valid(raise_exception=True)
        uuid = uuid_token_serializer.data.get('uuid')
        user = User.objects.get(uuid=uuid)
        serializer = self.serializer_class(data=request.data, instance=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangeUserFirstNameView(generics.GenericAPIView):
    """
    Изменение имени авторизированного пользователя
    """
    serializer_class = ChangeUserFirstNameSerializer
    permission_classes = [IsAuthenticated, ]
    renderer_classes = (UserDataRender,)

    def put(self, request):
        serializer = self.serializer_class(
            data=request.data, instance=request.user
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangeUserLastNameView(generics.GenericAPIView):
    """
    Изменение фамилии авторизированного пользователя
    """
    serializer_class = ChangeUserLastNameSerializer
    permission_classes = [IsAuthenticated, ]
    renderer_classes = (UserDataRender,)

    def put(self, request):
        serializer = self.serializer_class(
            data=request.data, instance=request.user
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangeUserPhoneNumberView(generics.GenericAPIView):
    """
    Изменение номера телефона авторизированного пользователя
    """
    serializer_class = ChangeUserPhoneNumberSerializer
    permission_classes = [IsAuthenticated, ]
    renderer_classes = (UserDataRender,)

    def put(self, request):
        serializer = self.serializer_class(
            data=request.data, instance=request.user
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangeUserPasswordView(generics.GenericAPIView):
    """
    Изменение пароля авторизированного пользователя
    """
    serializer_class = ChangeUserPasswordSerializer
    permission_classes = [IsAuthenticated, ]
    renderer_classes = (UserDataRender,)

    def put(self, request):
        serializer = self.serializer_class(
            data=request.data, instance=request.user
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangeUserEmailView(generics.GenericAPIView):
    """
    Изменение эл.почты авторизированного пользователя.
    На переданную электронную почту будет отправленна ссылка
    на изменение эл. почты, пока пользователь не перейдет по этой
    ссылке, почта не будет изменена
    """
    serializer_class = ChangeUserEmailSerializer
    throttle_classes = (AnonRateThrottle,)
    renderer_classes = (UserDataRender,)
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        NewEmail.objects.create(
            user_uuid_id=request.user.uuid, email=serializer.data.get('email')
        )
        data = get_data_for_add_new_email_for_user_email(
            email=serializer.data.get('email'),
            user=request.user,
            request=request
        )
        send_email_for_user.delay(
            data=data
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


class CheckTokenForChangeUserEmailView(generics.GenericAPIView):
    """
    Проверка данных в ссылке на изменение почты
    """
    permission_classes = [IsAuthenticated, ]
    renderer_classes = (UserDataRender,)
    serializer_class = UserTokenUIDSerializer

    def put(self, request, **kwargs):
        uidb64 = kwargs.get('uidb64', '')
        token = kwargs.get('token', '')
        serializer = self.serializer_class(
            data={
                'uidb64': uidb64,
                'token': token
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer_data = serializer.data
        uuid = serializer_data.get('uuid')
        try:
            new_email = NewEmail.objects.filter(user_uuid_id=uuid)
        except NewEmail.DoesNotExist:
            return Response(
                data={'link': 'A link is not valid.'},
                status=status.HTTP_404_NOT_FOUND
            )
        if str(request.user.uuid) == uuid:
            user = User.objects.get(uuid=uuid)
            user.email = new_email.first().email
            user.save()
            new_email.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            data={'uuid': 'An uuid is not valid.'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class ChangeUserUsenameView(generics.GenericAPIView):
    """
    Изменение юзернейма авторизированного пользователя
    """
    serializer_class = ChangeUserUsernameSerializer
    permission_classes = [IsAuthenticated, ]
    renderer_classes = (UserDataRender,)

    def put(self, request):
        serializer = self.serializer_class(
            data=request.data, instance=request.user
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
