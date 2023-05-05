from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from rest_framework.settings import api_settings
from djoser.serializers import UserCreateMixin


class CreateUserSerializer(UserCreateMixin, serializers.ModelSerializer):
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

    def validate(self, attrs: dict):
        password = attrs.get("password")
        password_confirm = attrs.get("password_confirm")
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

            return attrs
        raise serializers.ValidationError(
            {
                "password": 'The passwords entered do not match',
                "password_confirm": 'The passwords entered do not match'
            }
        )
