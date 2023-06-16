from typing import Any
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    def create_user(self, username, email, password):
        user = self.model(
            username=username,
            email=self.normalize_email(email=email),
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password):
        user = self.model(
            username=username,
            email=self.normalize_email(email=email),
        )
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractUser):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    email = models.EmailField(
        _("email address"),
        blank=True,
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        }
    )
    is_confirm = models.BooleanField(
        _("confirm"),
        default=False,
    )
    phone_number = models.CharField(
        _("phone number"),
        max_length=11,
        blank=True,
        error_messages={
            "unique": _("A user with that phone number already exists."),
            "max_length": _("A telephone number cannot have more than 11 digits"),
        }
    )

    objects = UserManager()

    def tokens(self):
        refresh_token = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh_token),
            'access': str(refresh_token.access_token)
        }