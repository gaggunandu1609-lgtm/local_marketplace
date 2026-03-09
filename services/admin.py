from django.contrib import admin
from .models import ServiceProvider

@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = (
        "provider_id",
        "full_name",
        "service_category",
        "city",
        "rating",
        "verified",
        "availability_status",
    )
    search_fields = ("full_name", "city", "service_category")
    list_filter = ("city", "verified", "availability_status")