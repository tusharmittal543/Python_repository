import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from drivers.models import Driver
from routes.models import Route
from trips.models import Trip
from vehicles.models import Vehicle


class TripLocationApiTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.driver_user = user_model.objects.create_user(username="driver", password="strong-pass-123")
        self.passenger = user_model.objects.create_user(username="passenger", password="strong-pass-123")
        self.other_user = user_model.objects.create_user(username="other", password="strong-pass-123")
        driver = Driver.objects.create(user=self.driver_user, full_name="Test Driver", license_number="LIC-100")
        route = Route.objects.create(name="Central line", origin="Central", destination="Harbor")
        vehicle = Vehicle.objects.create(registration_number="BUS-100", make="Example", model="City", capacity=30)
        self.trip = Trip.objects.create(
            route=route,
            vehicle=vehicle,
            driver=driver,
            scheduled_departure=timezone.now(),
            status=Trip.Status.IN_PROGRESS,
        )
        self.trip.passengers.add(self.passenger)
        self.url = f"/api/trips/{self.trip.pk}/locations/"

    def test_assigned_driver_can_post_valid_location(self):
        self.client.force_login(self.driver_user)
        response = self.client.post(self.url, data=json.dumps({"latitude": 40.7128, "longitude": -74.006}), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.trip.locations.count(), 1)

    def test_passenger_can_read_but_cannot_post_location(self):
        self.client.force_login(self.passenger)
        self.assertEqual(self.client.get(self.url).status_code, 200)
        response = self.client.post(self.url, data=json.dumps({"latitude": 40, "longitude": -74}), content_type="application/json")
        self.assertEqual(response.status_code, 403)

    def test_other_user_cannot_read_trip_location(self):
        self.client.force_login(self.other_user)
        self.assertEqual(self.client.get(self.url).status_code, 403)

    def test_out_of_range_coordinate_is_rejected(self):
        self.client.force_login(self.driver_user)
        response = self.client.post(self.url, data=json.dumps({"latitude": 91, "longitude": 0}), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.trip.locations.count(), 0)