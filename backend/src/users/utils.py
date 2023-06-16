from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from rest_framework.request import Request
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


def send_email(data: dict):
    """Функция для отправки сообщения пользователю"""
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
    token = RefreshToken.for_user(user).access_token
    current_site = get_current_site(request=request)
    email_body = render_to_string('confirm_account.html',
                                  {
                                      'user': user,
                                      'protocol': 'https' if request.is_secure() else 'http',
                                      'domain': current_site.domain,
                                      'token': token
                                  })
    return {
        'email_subject': 'Verify your account',
        'email_body': email_body,
        'email_recipient': (user.email,)
    }
