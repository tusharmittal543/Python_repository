from django.contrib import admin

from .models import Trip


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ("route", "scheduled_departure", "vehicle", "driver", "status")
    list_filter = ("status", "scheduled_departure", "route")
    search_fields = ("route__name", "vehicle__registration_number", "driver__full_name", "passengers__username")
    filter_horizontal = ("passengers",)
    date_hierarchy = "scheduled_departure"