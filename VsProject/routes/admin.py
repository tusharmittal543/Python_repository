from django.contrib import admin

from .models import Route, Stop


class StopInline(admin.TabularInline):
    model = Stop
    extra = 0


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ("name", "origin", "destination", "active")
    list_filter = ("active",)
    search_fields = ("name", "origin", "destination", "stops__name")
    inlines = (StopInline,)


@admin.register(Stop)
class StopAdmin(admin.ModelAdmin):
    list_display = ("name", "route", "sequence", "latitude", "longitude")
    list_filter = ("route",)