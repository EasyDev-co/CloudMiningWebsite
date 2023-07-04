from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.request import Request
from rest_framework_simplejwt.tokens import RefreshToken

from src.users.constants import (
    EMAIL_SUBJECT_FOR_ACTIVATION_ACCONT,
    EMAIL_SUBJECT_FOR_RESET_PASSWORD,
    EMAIL_SUBJECT_FOR_CHANGE_EMAIL
)

User = get_user_model()


def send_email(data: dict):
    """
    Отправляет сообщение пользователю
    """
    email_subject = data.get('email_subject')
    email_body = data.get('email_body')
    email_recipient = data.get('email_recipient')
    email = EmailMessage(
        subject=email_subject,
        body=email_body,
        to=email_recipient
    )
    email.send()


def get_data_for_activation_account_email(
        user: User,
        request: Request
):
    """
    Формирует данные письма с ссылкой для
    активации аккаунта
    """
    token = RefreshToken.for_user(user).access_token
    current_site = get_current_site(request=request)
    email_body = render_to_string(
        'confirm_account.html',
        {
            'user': user,
            'protocol': 'https' if request.is_secure() else 'http',
            'domain': current_site.domain,
            'token': token
        })
    return {
        'email_subject': EMAIL_SUBJECT_FOR_ACTIVATION_ACCONT,
        'email_body': email_body,
        'email_recipient': (user.email,)
    }


def get_data_for_reset_password_email(
        user: User,
        request: Request
):
    """
    Формирует данные письма с ссылкой для
    сброса пароля
    """
    uidb64 = urlsafe_base64_encode(force_bytes(user.uuid))
    token = PasswordResetTokenGenerator().make_token(user)
    current_site = get_current_site(request=request)
    email_body = render_to_string(
        'reset_password.html',
        {
            'user': user,
            'protocol': 'https' if request.is_secure() else 'http',
            'domain': current_site.domain,
            'token': token,
            'uidb64': uidb64
        })
    return {
        'email_subject': EMAIL_SUBJECT_FOR_RESET_PASSWORD,
        'email_body': email_body,
        'email_recipient': (user.email,)
    }


def get_data_for_add_new_email_for_user_email(
        email: str,
        user: User,
        request: Request
):
    """
    Формирует данные письма с ссылкой для
    изменения адреса почты
    """
    uidb64 = urlsafe_base64_encode(force_bytes(user.uuid))
    token = PasswordResetTokenGenerator().make_token(user)
    current_site = get_current_site(request=request)
    email_body = render_to_string(
        'change_email.html',
        {
            'user': user,
            'protocol': 'https' if request.is_secure() else 'http',
            'domain': current_site.domain,
            'token': token,
            'uidb64': uidb64
        })
    return {
        'email_subject': EMAIL_SUBJECT_FOR_CHANGE_EMAIL,
        'email_body': email_body,
        'email_recipient': (email,)
    }
