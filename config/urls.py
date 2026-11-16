"""
URL configuration for PCM Gatak website.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Kustomisasi judul dan header Django Admin sesuai spesifikasi A3 & Master Prompt
admin.site.site_header = "Admin Website PCM Gatak"
admin.site.site_title = "Admin PCM Gatak"
admin.site.index_title = "Panel Pengelolaan Konten Website PCM Gatak"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls', namespace='website')),
]

# Sajikan media uploads di mode development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
