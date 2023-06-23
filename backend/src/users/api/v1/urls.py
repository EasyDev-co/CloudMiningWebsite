from django.urls import path
from src.users.api.v1.views import (
    UserRegistrationView,
    UserActivationAccountView,
    ResendActivationAccountEmailView,
    UserLoginView,
    ResetPasswordView,
    CheckTokenForResetPasswordView,
    ChangeUserFirstNameView,
    ChangeUserLastNameView,
    ChangeUserPhoneNumberView,
    ChangeUserPasswordView,
    ChangeUserEmailView,
    CheckTokenForChangeUserEmailView,
    GetUserDataView,
    ChangeUserUsenameView
)
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path(
        'token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),

    path(
        'register/',
        UserRegistrationView.as_view(),
        name='register'
    ),

    path(
        'activation/<token>/',
        UserActivationAccountView.as_view(),
        name='activation'
    ),

    path(
        'activation/resend/<email>/',
        ResendActivationAccountEmailView.as_view(),
        name='resend_activation'
    ),

    path(
        'login/',
        UserLoginView.as_view(),
        name='login'
    ),

    path(
        'reset-password/<uidb64>/<token>/',
        CheckTokenForResetPasswordView.as_view(),
        name='confirm_for_reset_password'
    ),

    path(
        'reset-password/',
        ResetPasswordView.as_view(),
        name='send_email_for_reset'
    ),

    path(
        'change/first_name/',
        ChangeUserFirstNameView.as_view(),
        name='change_first_name'
    ),

    path(
        'change/last_name/',
        ChangeUserLastNameView.as_view(),
        name='change_last_name'
    ),

    path(
        'change/phone_number/',
        ChangeUserPhoneNumberView.as_view(),
        name='change_phone_number'
    ),

    path(
        'change/password/',
        ChangeUserPasswordView.as_view(),
        name='change_password'
    ),

    path(
        'change/email/',
        ChangeUserEmailView.as_view(),
        name='change_email'
    ),
    path(
        'change/email/<uidb64>/<token>/',
        CheckTokenForChangeUserEmailView.as_view(),
        name='confirm_for_change_email'
    ),
    path(
        'change/username/',
        ChangeUserUsenameView.as_view(),
        name='change_username'
    ),
    path(
        '',
        GetUserDataView.as_view(),
        name='user'
    )
]
