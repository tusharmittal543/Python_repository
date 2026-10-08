from django.contrib import admin

from .models import Driver


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ("full_name", "license_number", "phone", "user", "active")
    list_filter = ("active",)
    search_fields = ("full_name", "license_number", "phone", "user__username")