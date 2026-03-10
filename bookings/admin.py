from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("user", "service", "status", "booking_date", "total_amount")
    list_filter = ("status", "booking_date")
    search_fields = ("user__username", "service__name")
