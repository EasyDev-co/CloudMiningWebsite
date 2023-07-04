from django.urls import path, include

urlpatterns = [
    path('api/v1/reviews/', include('src.reviews.api.v1.urls')),
]
