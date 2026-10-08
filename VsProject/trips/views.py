from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .models import Trip


@login_required
def trip_detail(request, pk):
    trip = get_object_or_404(Trip.objects.select_related("route", "vehicle", "driver").prefetch_related("route__stops"), pk=pk)
    can_view = request.user.is_staff or trip.passengers.filter(pk=request.user.pk).exists()
    if trip.driver.user_id == request.user.pk:
        can_view = True
    if not can_view:
        raise Http404
    return render(request, "trips/detail.html", {"trip": trip})