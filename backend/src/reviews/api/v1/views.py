from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from src.reviews.api.v1.serializers import ReviewsSerializer, AddReviewForAnonymousAndWithoutDataUsersSerializer, AddReviewForAuthenticatedUsersWithDataSerializer
from src.reviews.models import Review
from django.contrib.auth.models import AnonymousUser


class ReviewsListPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 30


class AddReviewView(generics.CreateAPIView):
    """Добавление отзыва"""

    def create(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            serializer = AddReviewForAnonymousAndWithoutDataUsersSerializer(
                data=request.data
            )
        serializer.is_valid(raise_exception=True)
        serializer.save(
            author=request.user
        )
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
