from django.core.validators import MinValueValidator
from django.db import models


class Vehicle(models.Model):
    registration_number = models.CharField(max_length=20, unique=True)
    make = models.CharField(max_length=80)
    model = models.CharField(max_length=80)
    capacity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["registration_number"]

    def __str__(self):
        return f"{self.registration_number} ({self.make} {self.model})"