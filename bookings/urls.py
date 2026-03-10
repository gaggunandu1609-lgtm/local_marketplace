from django.urls import path
from .views import create_booking, booking_confirm, simulate_payment, payment_success_view, payment_cancel

urlpatterns = [
    path("book/<int:service_id>/", create_booking, name="create_booking"),
    path("confirm/<int:booking_id>/", booking_confirm, name="booking_confirm"),
    path("pay/<int:booking_id>/", simulate_payment, name="simulate_payment"),
    path("success/<int:booking_id>/", payment_success_view, name="payment_success_view"),
    path("cancel/", payment_cancel, name="payment_cancel"),
]