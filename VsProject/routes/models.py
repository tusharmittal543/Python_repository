from django.core.validators import MinValueValidator
from django.db import models


class Route(models.Model):
    name = models.CharField(max_length=120, unique=True)
    origin = models.CharField(max_length=160)
    destination = models.CharField(max_length=160)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}: {self.origin} to {self.destination}"


class Stop(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="stops")
    name = models.CharField(max_length=160)
    sequence = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    class Meta:
        ordering = ["sequence"]
        constraints = [models.UniqueConstraint(fields=["route", "sequence"], name="unique_stop_sequence_per_route")]

    def __str__(self):
        return f"{self.route.name} / {self.sequence}. {self.name}"