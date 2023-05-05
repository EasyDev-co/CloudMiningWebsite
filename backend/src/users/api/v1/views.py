from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from src.users.api.v1.serializers import CreateUserSerializer
from djoser.views import UserViewSet
from djoser.compat import get_user_email
from djoser.conf import settings
from rest_framework.decorators import action
from rest_framework.routers import DefaultRouter
from src.users.tasks import send_reset_password_email


class CustomUserViewSet(UserViewSet):
    # serializer_class = CreateUserSerializer

    @action(["post"], detail=False)
    def reset_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_user()
        print('Это моя функция')
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