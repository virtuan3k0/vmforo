from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('users.urls')),  # User-related endpoints
    path('forum/', include('forum.urls')),  # Forum-related endpoints
]
