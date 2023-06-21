from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from src.reviews.api.v1.serializers import ReviewsSerializer, AddReviewSerializer
from src.reviews.models import Review
from django.contrib.auth.models import AnonymousUser


class ReviewsListPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 30


class AddReviewView(generics.GenericAPIView):
    """Добавление отзыва"""
    serializer_class = AddReviewSerializer

    def get_data(self, request):
        if request.user.is_anonymous:
            return request.data

        elif request.user.is_authenticated:
            user_first_name = request.user.first_name
            user_last_name = request.user.last_name
            user_phone_number = request.user.phone_number

            return {
                'first_name': user_first_name if user_first_name else request.data.get('first_name'),
                'last_name': user_last_name if user_first_name else request.data.get('last_name'),
                'phone_number': user_phone_number if user_phone_number else request.data.get('phone_number')
            }

    def post(self, request, *args, **kwargs):
        data = self.get_data(request=request)
        serializer = self.serializer_class(
            data=data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
            )


class AllReviewsView(generics.ListAPIView):
    """Вывод всех отзывов, одобренных администратором"""
    serializer_class = ReviewsSerializer
    pagination_class = ReviewsListPagination

    def get_queryset(self):
        queryset = Review._default_manager.filter(
            is_published=True
        )
        return queryset


# Нужно изменить модель «Отзывы», убрать ссылку на пользователя
# Добавить поля имя, фамилия и номер телефона
# Во вьюхе нужно сделать проверку, что если пользователь не имеет
# своих данных и пишет отзыв, то брать из переданных данных и изменять
# данные пользователя