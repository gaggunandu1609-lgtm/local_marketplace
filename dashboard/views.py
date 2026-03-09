from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from bookings.models import Booking
from accounts.models import Profile


@login_required
def provider_dashboard(request):
    profile = Profile.objects.get(user=request.user)

    if profile.role != "provider":
        return redirect("/")

    bookings = Booking.objects.filter(service__provider=profile)

    return render(request, "provider_dashboard.html", {"bookings": bookings})


@login_required
def update_booking_status(request, booking_id, status):
    booking = Booking.objects.get(id=booking_id)

    booking.status = status
    booking.save()

    return redirect("provider_dashboard")