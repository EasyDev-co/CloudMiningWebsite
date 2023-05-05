from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from config.components.swagger import schema_view
from config.components.static import MEDIA_URL, MEDIA_ROOT
from config import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('', include('src.users.api.urls'))
]

if settings.DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
