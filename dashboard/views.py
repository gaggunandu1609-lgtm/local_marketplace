from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from bookings.models import Booking
from services.models import Service, ServiceProvider, Category
from accounts.models import Profile
from notifications.models import Notification
from django.db.models import Count, Sum
from django.contrib import messages

from tasks.models import Task, Quote

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
    quotes = Quote.objects.filter(provider=provider).select_related('task').order_by('-created_at')
    
    # Accurate Stats
    stats = {
        'total_services': services.count(),
        'total_bookings': bookings.count(),
        'pending_bookings': bookings.filter(status='pending').count(),
        'accepted_bookings': bookings.filter(status='accepted').count(),
        'completed_bookings': bookings.filter(status='completed').count(),
        'total_earnings': bookings.filter(status='completed').aggregate(Sum('total_amount'))['total_amount__sum'] or 0.00
    }

    # Simulation: Monthly earnings for chart
    monthly_data = [2500, 3200, 4100, 3800, 5200, 4800, 6100] # Dummy data for demo
    
    return render(request, "provider_dashboard.html", {
        "services": services,
        "bookings": bookings,
        "quotes": quotes,
        "stats": stats,
        "provider": provider,
        "monthly_data": monthly_data
    })

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "orders.html", {"bookings": bookings})

@login_required
def update_booking_status(request, booking_id, status):
    booking = get_object_or_404(Booking, id=booking_id)

    # Security check: only the provider of the service can update status
    provider = getattr(booking, 'provider', None)
    if provider and provider.user == request.user:
        allowed = ['accepted', 'in progress', 'completed', 'cancelled', 'pending payment']
        if status in allowed:
            booking.status = status
            booking.save()

            # Notify the customer
            status_msgs = {
                'accepted': f"Your booking for '{booking.service.name}' has been accepted!",
                'in progress': f"Pro is now working on your request for '{booking.service.name}'.",
                'completed': f"Service '{booking.service.name}' marked as completed. Please leave a review!",
                'cancelled': f"Sorry, your booking for '{booking.service.name}' was cancelled by the provider.",
                'pending payment': f"Booking for '{booking.service.name}' is pending payment."
            }
            
            if status in status_msgs:
                Notification.objects.create(
                    user=booking.user,
                    title=f"Booking Update: {status.title()}",
                    message=status_msgs[status],
                    link=reverse('my_bookings')
                )

        if status == 'completed':
            provider.availability = 'Available'
            provider.save()

        if request.headers.get('HX-Request'):
            source = request.GET.get('source', 'dashboard')
            if source == 'bookings':
                return render(request, "partials/booking_row_bookings.html", {"booking": booking})
            return render(request, "partials/booking_row_dashboard.html", {"booking": booking})

        messages.success(request, f"Booking status updated to {status}.")
    else:
        if not request.headers.get('HX-Request'):
            messages.error(request, "You do not have permission to update this booking.")

    return redirect(request.META.get('HTTP_REFERER', 'provider_dashboard'))

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.status in ['pending', 'accepted']:
        booking.status = 'cancelled'
        booking.save()
        
        # Notify provider
        Notification.objects.create(
            user=booking.provider.user,
            title="Booking Cancelled",
            message=f"Customer {request.user.username} has cancelled the booking for '{booking.service.name}'.",
            link=reverse('provider_dashboard')
        )
        
        if request.headers.get('HX-Request'):
            return render(request, "partials/order_row.html", {"booking": booking})
            
        messages.success(request, "Booking cancelled successfully.")
    else:
        if not request.headers.get('HX-Request'):
            messages.error(request, "This booking cannot be cancelled.")
        
    return redirect('my_bookings')

@login_required
def provider_profile(request):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    categories = Category.objects.all()
    from services.models import City
    cities = City.objects.all()

    if request.method == "POST":
        provider.phone_number = request.POST.get('phone_number', provider.phone_number)
        provider.description = request.POST.get('bio', provider.description)
        provider.experience_years = request.POST.get('experience_years', provider.experience_years)
        
        category_id = request.POST.get('category')
        if category_id:
            try:
                provider.category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                pass
            
        city_id = request.POST.get('city')
        if city_id:
            try:
                provider.city_ref = City.objects.get(id=city_id)
            except City.DoesNotExist:
                pass
        
        if request.FILES.get('profile_photo'):
            provider.profile_photo = request.FILES.get('profile_photo')
            
        provider.save()
        
        # Update user name
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        if first_name is not None:
            request.user.first_name = first_name
        if last_name is not None:
            request.user.last_name = last_name
        request.user.save()

        messages.success(request, "Profile updated successfully!")
        return redirect("provider_profile")

    return render(request, "provider_profile.html", {"provider": provider, "categories": categories, "cities": cities})

@login_required
def provider_portfolio(request):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    from services.models import PortfolioImage
    images = PortfolioImage.objects.filter(provider=provider)
    return render(request, "provider_portfolio.html", {"provider": provider, "portfolio_images": images})

@login_required
def update_portfolio(request):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    from services.models import PortfolioImage
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "add" and request.FILES.get("image"):
            PortfolioImage.objects.create(
                provider=provider,
                image=request.FILES.get("image"),
                caption=request.POST.get("caption", "")
            )
            messages.success(request, "Image added to portfolio!")
        elif action == "delete":
            image_id = request.POST.get("image_id")
            PortfolioImage.objects.filter(id=image_id, provider=provider).delete()
            messages.success(request, "Image deleted from portfolio!")
            
    return redirect("provider_portfolio")

@login_required
def provider_reviews(request):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    from reviews.models import Review
    # Get all reviews for services owned by this provider
    reviews = Review.objects.filter(service__provider=provider).order_by('-created_at')
    return render(request, "provider_reviews.html", {"provider": provider, "reviews": reviews})

@login_required
def provider_services(request):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    services = Service.objects.filter(provider=provider).order_by('-created_at')
    return render(request, "provider_services.html", {"services": services, "provider": provider})

@login_required
def provider_bookings(request):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    # Get all bookings for services owned by this provider
    bookings = Booking.objects.filter(service__provider=provider).select_related('user', 'service').order_by('-created_at')
    return render(request, "provider_bookings.html", {"bookings": bookings, "provider": provider})

@login_required
def add_service(request):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    categories = Category.objects.all()
    
    if request.method == "POST":
        name = request.POST.get("name")
        category_id = request.POST.get("category")
        price = request.POST.get("price")
        description = request.POST.get("description")
        image = request.FILES.get("image")
        portfolio_images = request.FILES.get("portfolio_images")
        
        category = get_object_or_404(Category, id=category_id)
        
        Service.objects.create(
            provider=provider,
            name=name,
            category=category,
            price=price,
            description=description,
            image=image,
            portfolio_images=portfolio_images,
            city=provider.city_ref.name if provider.city_ref else "",
            area=provider.area
        )
        
        messages.success(request, "Service added successfully!")
        return redirect("provider_dashboard")
        
    return render(request, "add_service.html", {"categories": categories})

@login_required
def edit_service(request, service_id):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    service = get_object_or_404(Service, id=service_id, provider=provider)
    categories = Category.objects.all()
    
    # HTMX Inline Edit Request (GET)
    if request.headers.get('HX-Request') and request.method == "GET":
        if request.GET.get('cancel'):
            return render(request, "partials/service_row.html", {"service": service})
        return render(request, "partials/edit_service_row.html", {"service": service, "categories": categories})

    if request.method == "POST":
        service.name = request.POST.get("name")
        category_id = request.POST.get("category")
        service.category = get_object_or_404(Category, id=category_id)
        service.price = request.POST.get("price")
        
        # Description and images only updated in full form
        if not request.headers.get('HX-Request'):
            service.description = request.POST.get("description")
            if request.FILES.get("image"):
                service.image = request.FILES.get("image")
            if request.FILES.get("portfolio_images"):
                service.portfolio_images = request.FILES.get("portfolio_images")
        
        service.save()
        
        if request.headers.get('HX-Request'):
            return render(request, "partials/service_row.html", {"service": service})
            
        messages.success(request, "Service updated successfully!")
        return redirect("provider_dashboard")
        
    return render(request, "add_service.html", {"service": service, "categories": categories, "edit": True})

@login_required
def delete_service(request, service_id):
    provider = get_object_or_404(ServiceProvider, user=request.user)
    service = get_object_or_404(Service, id=service_id, provider=provider)
    service.delete()
    
    if request.headers.get('HX-Request'):
        from django.http import HttpResponse
        return HttpResponse("")
        
    messages.success(request, "Service deleted successfully!")
    return redirect("provider_dashboard")