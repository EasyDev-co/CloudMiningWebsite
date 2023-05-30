from rest_framework import status
from rest_framework.response import Response
from djoser.views import UserViewSet
from djoser.compat import get_user_email
from rest_framework.decorators import action
from src.users.tasks import send_reset_password_email


class CustomUserViewSet(UserViewSet):

    @action(["post"], detail=False)
    def reset_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_user()
        if user:
            send_reset_password_email.delay(
                {
                    'user_id': user.id,
                    'domain': request.get_host(),
                    'protocol': 'https' if request.is_secure() else 'http',
                    'site_name': request.get_host()
                },
                [get_user_email(user)]
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    def me(self):
        pass

    def activation(self):
        pass

    def resend_activation(self):
        pass

    def reset_username(self):
        pass

    def reset_username_confirm(self):
        pass

    def set_username(self):
        pass
