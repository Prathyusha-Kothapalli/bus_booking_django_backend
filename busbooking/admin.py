from django.contrib import admin
from .models import Bus, Seat


class BusAdmin(admin.ModelAdmin):
    list_display = "bus_name", "number", "origin", "destination"
admin.site.register(Bus, BusAdmin)

class SeatAdmin(admin.ModelAdmin):
    list_display = "bus", "seat_number", "is_booked"
admin.site.register(Seat, SeatAdmin)

# Register your models here.
