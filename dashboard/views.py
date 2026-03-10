from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from bookings.models import Booking
from services.models import Service, ServiceProvider, Category
from accounts.models import Profile
from notifications.models import Notification
from django.db.models import Count, Sum
from django.contrib import messages

@login_required
def provider_dashboard(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        # Fallback if profile is missing
        profile = Profile.objects.create(user=request.user, role='customer')
        return redirect("/")

    if profile.role != "provider":
        messages.warning(request, "Access denied. Only service providers can view this dashboard.")
        return redirect("/")

    provider, created = ServiceProvider.objects.get_or_create(user=request.user, defaults={'business_name': f"{request.user.username}'s Services"})
    
    # Mark notification as read when viewing dashboard
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    
    if request.method == "POST" and "availability" in request.POST:
        new_status = request.POST.get("availability")
        if new_status in dict(ServiceProvider.AVAILABILITY_CHOICES).keys():
            provider.availability = new_status
            provider.save()
            messages.success(request, f"Availability tracked successfully as {new_status}")
            return redirect("provider_dashboard")
            
    # We prefer looking up by the provider object directly
    services = Service.objects.filter(provider=provider)
    bookings = Booking.objects.filter(service__provider=provider).select_related('user', 'service').order_by('-created_at')
    
    # Accurate Stats
    stats = {
        'total_services': services.count(),
        'total_bookings': bookings.count(),
        'pending_bookings': bookings.filter(status='Pending').count(),
        'accepted_bookings': bookings.filter(status='Accepted').count(),
        'completed_bookings': bookings.filter(status='Completed').count(),
        'total_earnings': bookings.filter(status='Completed').aggregate(Sum('total_amount'))['total_amount__sum'] or 0.00
    }

    return render(request, "provider_dashboard.html", {
        "services": services,
        "bookings": bookings,
        "stats": stats,
        "provider": provider
    })

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "orders.html", {"bookings": bookings})

@login_required
def update_booking_status(request, booking_id, status):
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Security check: only the provider of the service can update status
    if booking.service.provider.user == request.user:
        booking.status = status
        booking.save()
        
        # Simulate availability logic
        if status in ['Completed', 'Rejected']:
            provider = booking.service.provider
            provider.availability = 'Available'
            provider.save()
            
        messages.success(request, f"Booking for {booking.service.name} has been {status.lower()}.")
    else:
        messages.error(request, "You do not have permission to update this booking.")

    return redirect("provider_dashboard")

@login_required
def add_service(request):
    try:
        provider = ServiceProvider.objects.get(user=request.user)
    except ServiceProvider.DoesNotExist:
        return redirect("provider_dashboard")

    if request.method == "POST":
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        Service.objects.create(
            provider=provider,
            name=name,
            category_id=category_id,
            price=price,
            description=description,
            image=image
        )
        messages.success(request, "Service added successfully!")
        return redirect("provider_dashboard")

    categories = Category.objects.all()
    return render(request, "add_service.html", {"categories": categories})

@login_required
def edit_service(request, service_id):
    service = get_object_or_404(Service, id=service_id, provider__user=request.user)
    
    if request.method == "POST":
        service.name = request.POST.get('name')
        service.category_id = request.POST.get('category')
        service.price = request.POST.get('price')
        service.description = request.POST.get('description')
        if request.FILES.get('image'):
            service.image = request.FILES.get('image')
        
        service.save()
        messages.success(request, "Service updated successfully!")
        return redirect("provider_dashboard")

    categories = Category.objects.all()
    return render(request, "add_service.html", {"service": service, "categories": categories, "edit": True})

@login_required
def delete_service(request, service_id):
    service = get_object_or_404(Service, id=service_id, provider__user=request.user)
    service.delete()
    messages.success(request, "Service deleted successfully!")
    return redirect("provider_dashboard")