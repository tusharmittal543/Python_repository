from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from django.shortcuts import render
from django.utils import timezone

from trips.models import Trip
from vehicles.models import Vehicle
from drivers.models import Driver
from routes.models import Route


@login_required
def dashboard(request):
    trips = Trip.objects.select_related("route", "vehicle", "driver")
    if not request.user.is_staff:
        trips = trips.filter(passengers=request.user)
    trips = trips[:25]
    return render(request, "accounts/dashboard.html", {"trips": trips})


@user_passes_test(lambda user: user.is_staff)
def reports(request):
    today = timezone.localdate()
    trip_summary = Trip.objects.values("status").annotate(total=Count("id")).order_by("status")
    context = {
        "trip_summary": trip_summary,
        "active_trips": Trip.objects.filter(status=Trip.Status.IN_PROGRESS).select_related("route", "vehicle", "driver"),
        "today_trips": Trip.objects.filter(scheduled_departure__date=today).count(),
        "vehicle_count": Vehicle.objects.count(),
        "active_vehicle_count": Vehicle.objects.filter(active=True).count(),
        "driver_count": Driver.objects.filter(active=True).count(),
        "route_count": Route.objects.filter(active=True).count(),
    }
    return render(request, "accounts/reports.html", context)