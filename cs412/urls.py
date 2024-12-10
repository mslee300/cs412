from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('quotes.urls')),
    path('restaurant/', include('restaurant.urls')),
    path('voter_analytics/', include('voter_analytics.urls')),
    path('project/', include('project.urls')),
]

# This is for serving media files during development
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)