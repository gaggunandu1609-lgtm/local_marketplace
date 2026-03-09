from django.urls import path
from .views import provider_dashboard, update_booking_status

urlpatterns = [
    path("", provider_dashboard, name="provider_dashboard"),
    path("update/<int:booking_id>/<str:status>/", update_booking_status, name="update_booking_status"),
]