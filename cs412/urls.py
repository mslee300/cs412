from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('quotes.urls')),
    path('restaurant/', include('restaurant.urls')),
    path('mini_fb/', include('mini_fb.urls')),
]
