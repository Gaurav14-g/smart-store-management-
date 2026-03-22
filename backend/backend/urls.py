from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from api.health import health_check

urlpatterns = [
    path('', health_check, name='health-check'),
    path('api/v1/', include('api.urls')),
    path('auth/', include('security.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
