from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Trip(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = "scheduled", "Scheduled"
        IN_PROGRESS = "in_progress", "In progress"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    route = models.ForeignKey("routes.Route", on_delete=models.PROTECT, related_name="trips")
    vehicle = models.ForeignKey("vehicles.Vehicle", on_delete=models.PROTECT, related_name="trips")
    driver = models.ForeignKey("drivers.Driver", on_delete=models.PROTECT, related_name="trips")
    passengers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="passenger_trips")
    scheduled_departure = models.DateTimeField()
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.SCHEDULED)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-scheduled_departure"]

    def clean(self):
        if self.started_at and self.completed_at and self.completed_at < self.started_at:
            raise ValidationError({"completed_at": "Completion must be after the trip starts."})
    def save(self, *args, **kwargs):
        if self.status == self.Status.IN_PROGRESS and not self.started_at:
            self.started_at = timezone.now()
        if self.status == self.Status.COMPLETED and not self.completed_at:
            self.completed_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.route.name} - {self.scheduled_departure:%Y-%m-%d %H:%M}"