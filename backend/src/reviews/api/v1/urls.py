from django.urls import path
from src.reviews.api.v1.views import AllReviewsView, AddReviewView

urlpatterns = [
    path('reviews/add/', AddReviewView.as_view(), name='review-add'),
    path('reviews/', AllReviewsView.as_view(), name='reviews'),
]