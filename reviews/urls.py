from django.urls import path
from . import views

from .views import submit_review

urlpatterns = [
    path("submit/<int:booking_id>/", submit_review, name="submit_review"),
]
