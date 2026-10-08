from django.contrib import admin

from .models import Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("registration_number", "make", "model", "capacity", "active")
    list_filter = ("active", "make")
    search_fields = ("registration_number", "make", "model")