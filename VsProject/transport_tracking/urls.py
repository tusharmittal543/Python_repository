from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("accounts.urls")),
    path("trips/", include("trips.urls")),
    path("api/", include("tracking.urls")),
]