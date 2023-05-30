from django.urls import path, include

urlpatterns = [
    path('api/v1/', include('src.application.api.v1.urls')),
]
