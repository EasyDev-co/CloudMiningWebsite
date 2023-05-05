from django.urls import path, include, re_path
from src.users.api.v1.views import CustomUserViewSet
from django.contrib.auth import get_user_model
from rest_framework.routers import DefaultRouter
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
#     TokenVerifyView
# )


router = DefaultRouter()
router.register("users", CustomUserViewSet)

User = get_user_model()


urlpatterns = [
    # path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    re_path(r'^auth/', include('djoser.urls.jwt'))
]

urlpatterns += router.urls