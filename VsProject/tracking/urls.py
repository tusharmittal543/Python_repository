from django.urls import path

from . import views

app_name = "tracking"

urlpatterns = [path("trips/<int:trip_id>/locations/", views.trip_locations, name="trip-locations")]