from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", include("services.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("services/", include("services.urls")),
    path("bookings/", include("bookings.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
]