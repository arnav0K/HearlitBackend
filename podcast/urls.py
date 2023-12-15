from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-user/', include('Accounts.urls')),
    path('api-podcast/', include('Main.urls')),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
