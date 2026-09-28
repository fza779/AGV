"""URL configuration for the AGV project."""

from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/fza/", include("fza.urls")),
]
