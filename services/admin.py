from django.contrib import admin
from .models import ServiceProvider, Service, Category, City, PortfolioImage

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'state')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')

@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ("business_name", "city_ref", "rating", "verified", "availability")
    search_fields = ("business_name", "city_ref__name")
    list_filter = ("city_ref", "verified", "availability")

@admin.register(PortfolioImage)
class PortfolioImageAdmin(admin.ModelAdmin):
    list_display = ("provider", "caption")

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "provider", "category", "price", "is_active")
    search_fields = ("name", "description")
    list_filter = ("category", "is_active")