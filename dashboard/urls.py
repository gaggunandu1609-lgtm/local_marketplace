from django.urls import path
from .views import provider_dashboard, update_booking_status, my_bookings, add_service, edit_service, delete_service

urlpatterns = [
    path("", provider_dashboard, name="provider_dashboard"),
    path("my-bookings/", my_bookings, name="my_bookings"),
    path("update/<int:booking_id>/<str:status>/", update_booking_status, name="update_booking_status"),
    path("service/add/", add_service, name="add_service"),
    path("service/edit/<int:service_id>/", edit_service, name="edit_service"),
    path("service/delete/<int:service_id>/", delete_service, name="delete_service"),
]