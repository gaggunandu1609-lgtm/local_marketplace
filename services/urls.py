from django.urls import path
from .views import home, services_view, service_detail

urlpatterns = [
    path("", home, name="home"),
    path("services/", services_view, name="services"),
    path("service/<int:provider_id>/", service_detail, name="service_detail"),
]