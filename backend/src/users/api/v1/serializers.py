import jwt
from rest_framework import serializers, exceptions
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from rest_framework.settings import api_settings
from djoser.serializers import UserCreateMixin, UidAndTokenSerializer
from django.contrib.auth import get_user_model, authenticate
from django.core.validators import EmailValidator
from django.conf import settings

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    """Сериализация при регистрации пользователя"""

    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )
    password_confirm = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password_confirm']

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        password: str = attrs.get("password", '')
        password_confirm: str = attrs.get("password_confirm", '')
        attrs.pop('password_confirm')
        user = User(**attrs)

        if password == password_confirm:
            try:
                validate_password(password, user)
            except django_exceptions.ValidationError as e:
                serializer_error = serializers.as_serializer_error(e)
                raise serializers.ValidationError(
                    {"password": serializer_error[
                        api_settings.NON_FIELD_ERRORS_KEY
                    ]
                    }
                )

            return validated_data
        raise serializers.ValidationError(
            {
                "password": 'The passwords entered do not match',
                "password_confirm": 'The passwords entered do not match'
            }
        )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserActivationAccountSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True)
    uuid = serializers.CharField(read_only=True)

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        token = attrs.get('token', '')
        try:
            token_data = jwt.decode(
                token,
                settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(pk=token_data.get('user_uuid'))
        except (User.DoesNotExist, ValueError, TypeError, OverflowError, jwt.DecodeError):
            raise exceptions.NotAcceptable(
                {"link": 'An activation link is invalid'}
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.NotAcceptable(
                {'link': 'An activation link has expired'}
            )
        validated_data['uuid'] = user.uuid
        return validated_data


class ResendActivationAccountEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[EmailValidator, ])

    class Meta:
        model = User
        fields = ['email', ]

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        email = attrs.get('email', '')
        try:
            user = self.Meta.model.objects.get(email=email)
        except User.DoesNotExist:
            raise exceptions.NotFound(
                detail={'user': 'A user does not exist'}
            )
        if user.is_confirm:
            raise exceptions.NotFound(
                detail={'user': 'A user is already confirm'}
            )
        return validated_data


class LoginUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )
    username = serializers.CharField(write_only=True)
    tokens = serializers.DictField(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'tokens']

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        username = attrs.get('username', '')
        password = attrs.get('password', '')
        user = authenticate(username=username, password=password)
        if not user:
            raise exceptions.ValidationError(
                detail={
                    "new_password": 'Invalid credential',
                    "repeat_new_password": 'Invalid credential'
                }
            )
        if not user.is_confirm:
            raise exceptions.ValidationError(
                detail='An account is not confirm'
            )
        validated_data['tokens'] = user.tokens
        return validated_data


class PasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(style={"input_type": "password"})
    repeat_new_password = serializers.CharField(
        style={"input_type": "password"})
    user = serializers

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        new_password = attrs.get("new_password")
        repeat_new_password = attrs.get('repeat_new_password')
        if new_password == repeat_new_password:
            user = getattr(self, "user", None) or self.context["request"].user
            # why assert? There are ValidationError / fail everywhere
            assert user is not None

            try:
                validate_password(attrs["new_password"], user)
            except django_exceptions.ValidationError as e:
                raise serializers.ValidationError(
                    {"new_password": list(e.messages)})
            return validated_data
        raise serializers.ValidationError(
            {
                "new_password": 'The passwords entered do not match',
                "repeat_new_password": 'The passwords entered do not match'
            }
        )


class ResetPasswordSerializer(UidAndTokenSerializer, PasswordSerializer):
    pass
