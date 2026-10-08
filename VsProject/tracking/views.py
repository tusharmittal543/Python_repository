import json
from decimal import Decimal, InvalidOperation

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from trips.models import Trip
from .models import GPSLocation


def _can_view(user, trip):
    return user.is_staff or trip.passengers.filter(pk=user.pk).exists() or trip.driver.user_id == user.pk


@login_required
@require_http_methods(["GET", "POST"])
def trip_locations(request, trip_id):
    trip = get_object_or_404(Trip.objects.select_related("driver"), pk=trip_id)
    if not _can_view(request.user, trip):
        return JsonResponse({"error": "Not authorized for this trip."}, status=403)

    if request.method == "GET":
        points = trip.locations.order_by("-recorded_at")[:50]
        return JsonResponse({"locations": [
            {"latitude": str(point.latitude), "longitude": str(point.longitude), "recorded_at": point.recorded_at.isoformat()}
            for point in reversed(list(points))
        ]})

    if not (request.user.is_staff or trip.driver.user_id == request.user.pk):
        return JsonResponse({"error": "Only the assigned driver or staff can submit locations."}, status=403)
    if trip.status != Trip.Status.IN_PROGRESS:
        return JsonResponse({"error": "Locations can only be submitted for an in-progress trip."}, status=409)
    try:
        payload = json.loads(request.body)
        latitude = Decimal(str(payload["latitude"]))
        longitude = Decimal(str(payload["longitude"]))
        if not latitude.is_finite() or not longitude.is_finite() or not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
            raise ValueError
    except (json.JSONDecodeError, KeyError, TypeError, InvalidOperation, ValueError):
        return JsonResponse({"error": "Provide numeric latitude and longitude within valid coordinate ranges."}, status=400)

    point = GPSLocation(trip=trip, latitude=latitude, longitude=longitude)
    try:
        point.full_clean()
    except ValidationError:
        return JsonResponse({"error": "Coordinates do not fit the supported precision."}, status=400)
    point.save()
    return JsonResponse({
        "latitude": str(point.latitude),
        "longitude": str(point.longitude),
        "recorded_at": point.recorded_at.isoformat(),
    }, status=201)