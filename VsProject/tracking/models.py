from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class GPSLocation(models.Model):
    trip = models.ForeignKey("trips.Trip", on_delete=models.CASCADE, related_name="locations")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.DecimalField(max_digits=9, decimal_places=6, validators=[MinValueValidator(-180), MaxValueValidator(180)])
    recorded_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-recorded_at"]
        indexes = [models.Index(fields=["trip", "-recorded_at"], name="gps_trip_recent_idx")]

    def __str__(self):
        return f"{self.trip} @ {self.recorded_at:%Y-%m-%d %H:%M:%S}"