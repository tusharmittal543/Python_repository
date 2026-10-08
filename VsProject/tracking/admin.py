from django.contrib import admin

from .models import GPSLocation


@admin.register(GPSLocation)
class GPSLocationAdmin(admin.ModelAdmin):
    list_display = ("trip", "latitude", "longitude", "recorded_at")
    list_filter = ("recorded_at",)
    search_fields = ("trip__route__name",)
    readonly_fields = ("recorded_at",)