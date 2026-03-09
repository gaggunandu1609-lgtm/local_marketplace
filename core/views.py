from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Service, Booking


def home(request):
    return render(request, "home.html")


def service_list(request):
    services = Service.objects.all()
    return render(request, "services.html", {"services": services})


@login_required
def book_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)

    Booking.objects.create(
        customer=request.user,
        service=service
    )

    return redirect("my_bookings")


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(customer=request.user)
    return render(request, "my_bookings.html", {"bookings": bookings})