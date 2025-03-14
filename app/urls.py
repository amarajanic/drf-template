"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.db import OperationalError, connection
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from auth import urls as auth_urls
from users import urls as users_urls
from django.http import JsonResponse
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema


@extend_schema(responses={200: 'Health check OK', 503: 'Service Unavailable'})
@api_view(['GET'])
def health_check(request):
    try:
        connection.ensure_connection()
        return JsonResponse({'status': 'ok'})
    except OperationalError:
        return JsonResponse({'status': 'error', 'details': 'Database is down'}, status=500)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api_schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger-ui/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/', include(auth_urls)),
    path('users/', include(users_urls)),
    path('health-check/', health_check, name='health-check'),
]




