from django.urls import path
from .views import provider_dashboard, update_booking_status, my_bookings, cancel_booking, provider_profile, provider_portfolio, update_portfolio, provider_reviews, add_service, edit_service, delete_service, provider_services, provider_bookings

urlpatterns = [
    path("", provider_dashboard, name="provider_dashboard"),
    path("profile/", provider_profile, name="provider_profile"),
    path("portfolio/", provider_portfolio, name="provider_portfolio"),
    path("portfolio/update/", update_portfolio, name="update_portfolio"),
    path("reviews/", provider_reviews, name="provider_reviews"),
    path("services/", provider_services, name="provider_services"),
    path("bookings/", provider_bookings, name="provider_bookings"),
    path("my-bookings/", my_bookings, name="my_bookings"),
    path("update/<int:booking_id>/<str:status>/", update_booking_status, name="update_booking_status"),
    path("cancel/<int:booking_id>/", cancel_booking, name="cancel_booking"),
    path("add-service/", add_service, name="add_service"),
    path("edit-service/<int:service_id>/", edit_service, name="edit_service"),
    path("delete-service/<int:service_id>/", delete_service, name="delete_service"),
]