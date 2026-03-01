from django.contrib import admin
from django.urls import path, include
from api.health import health_check

urlpatterns = [
    path('', health_check, name='health-check'),
    # path('admin/', admin.site.urls),
    path('api/v1/',include('api.urls')),
    path('auth/',include('security.urls')),
    # path('api-auth/',include('rest_framework.urls',namespace='rest_framework')), # it will show login on admin panel on top-right corner of api, in which user doesnot need to be staff or admin
]
