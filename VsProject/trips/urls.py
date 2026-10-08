from django.urls import path

from . import views

app_name = "trips"

urlpatterns = [path("<int:pk>/", views.trip_detail, name="detail")]