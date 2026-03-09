from django.contrib import admin
from .models import ServiceCategory, ServiceProvider, Service, Booking

admin.site.register(ServiceCategory)
admin.site.register(ServiceProvider)
admin.site.register(Service)
admin.site.register(Booking)