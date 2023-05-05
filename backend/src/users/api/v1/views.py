from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from src.users.api.v1.serializers import CreateUserSerializer


class CreateUserView(generics.CreateAPIView):
    """Создание нового пользователя"""
    serializer_class = CreateUserSerializer
