from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

from dashboard.views import my_bookings
from bookings.views import create_booking
from accounts.views import custom_login

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("", include("services.urls")),
    path("bookings/", include("bookings.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("reviews/", include("reviews.urls")),
    path("tasks/", include("tasks.urls")),
    path("notifications/", include("notifications.urls")),
    path("chat/", include("chat.urls")),
    path("my-orders/", my_bookings, name="my_orders"),
    path("book/<int:service_id>/", create_booking, name="book_service"),
    path("login/", custom_login, name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)