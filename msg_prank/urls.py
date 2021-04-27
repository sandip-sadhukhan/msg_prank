from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('combat/', admin.site.urls),
    path('', include('website.urls')),
]
