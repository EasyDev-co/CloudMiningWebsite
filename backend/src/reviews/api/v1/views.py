from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from src.reviews.api.v1.serializers import (
    ReviewsSerializer,
    AddReviewLogicSerializer,
    AddReviewSerializer
)
from src.reviews.models import Review
from django.contrib.auth import get_user_model


User = get_user_model()


class ReviewsListPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 30


class AddReviewView(generics.GenericAPIView):
    """Добавление отзыва"""

    serializer_class = AddReviewSerializer

    def get_author_data(self, request):
        if request.user.is_anonymous:
            return request.data

        elif request.user.is_authenticated:
            uuid = request.user.uuid
            user = User.objects.get(uuid=uuid)
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            phone_number = request.data.get('phone_number')

            if not user.first_name and first_name:
                user.first_name = first_name
                user.save()
            if not user.last_name and last_name:
                user.last_name = last_name
                user.save()
            if not user.phone_number and phone_number:
                user.phone_number = phone_number
                user.save()

            return {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone_number': user.phone_number,
                'rating': request.data.get('rating'),
                'text': request.data.get('text')
            }

    def post(self, request, *args, **kwargs):
        data = self.get_author_data(request=request)
        serializer = AddReviewLogicSerializer(
            data=data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
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
