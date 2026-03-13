from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task, Quote
from services.models import City, ServiceProvider, Category
from bookings.models import Booking
from django.contrib import messages
from django.urls import reverse
from notifications.models import Notification

@login_required
def post_task(request):
    if request.method == "POST":
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        budget = request.POST.get('budget')
        city_id = request.POST.get('city')
        location_details = request.POST.get('location_details')
        preferred_date = request.POST.get('preferred_date')
        
        task = Task.objects.create(
            customer=request.user,
            category_id=category_id,
            title=title,
            description=description,
            budget=budget,
            city_ref_id=city_id,
            location_details=location_details,
            preferred_date=preferred_date,
            status='Open'
        )

        # Notify relevant providers in the same city and category
        matching_providers = ServiceProvider.objects.filter(
            city_ref_id=city_id,
            services__category_id=category_id
        ).distinct()
        
        for provider in matching_providers:
            if provider.user != request.user: # Don't notify self if they happen to be a provider
                Notification.objects.create(
                    user=provider.user,
                    title="🆕 New Task in your area!",
                    message=f"A new task '{title}' matching your expertise was posted in {task.city_ref.name}.",
                    link=reverse('task_detail', args=[task.id])
                )

        messages.success(request, "Your task has been posted successfully!")
        return redirect('my_tasks')
        
    cities = City.objects.all()
    categories = Category.objects.all()
    return render(request, "tasks/post_task.html", {"cities": cities, "categories": categories})

@login_required
def task_list(request):
    # For providers to see open tasks in their city and matching their expertise
    try:
        provider = request.user.provider_profile
        # Get all categories this provider offers
        provider_categories = provider.services.values_list('category', flat=True)
        
        tasks = Task.objects.filter(
            status='Open', 
            city_ref=provider.city_ref,
            category__in=provider_categories
        ).order_by('-created_at')
    except ServiceProvider.DoesNotExist:
        # Customers see their own tasks
        tasks = Task.objects.filter(customer=request.user).order_by('-created_at')
        
    return render(request, "tasks/task_list.html", {"tasks": tasks})

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    quotes = task.quotes.all()
    
    is_provider = hasattr(request.user, 'provider_profile')
    
    if request.method == "POST" and is_provider:
        proposed_price = request.POST.get('proposed_price')
        message = request.POST.get('message')
        
        quote = Quote.objects.create(
            task=task,
            provider=request.user.provider_profile,
            proposed_price=proposed_price,
            message=message
        )
        
        # Notify customer
        Notification.objects.create(
            user=task.customer,
            title="🏷️ New Quote Received!",
            message=f"{request.user.provider_profile.business_name} sent a quote of ₹{proposed_price} for your task '{task.title}'.",
            link=reverse('task_detail', args=[task.id])
        )
        
        messages.success(request, "Your quote has been sent!")
        return redirect('task_detail', task_id=task.id)
        
    return render(request, "tasks/task_detail.html", {
        "task": task,
        "quotes": quotes,
        "is_provider": is_provider
    })

@login_required
def my_tasks(request):
    tasks = Task.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, "tasks/my_tasks.html", {"tasks": tasks})

@login_required
def accept_quote(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id, task__customer=request.user)
    task = quote.task
    
    # Check if task is already closed
    if task.status != 'Open':
        messages.warning(request, "This task is no longer open.")
        return redirect('task_detail', task_id=task.id)
    
    # Try to find a matching service from the provider, or use the first one
    service = quote.provider.services.filter(category=task.category).first()
    if not service:
        service = quote.provider.services.first()
        
    if not service:
        messages.error(request, "Provider does not have any active services to book.")
        return redirect('task_detail', task_id=task.id)
    
    # Create Booking
    booking = Booking.objects.create(
        user=request.user,
        service=service,
        provider=quote.provider,
        task=task,
        booking_date=task.preferred_date,
        address=task.location_details,
        description=f"Booking for task: {task.title}\nDetails: {task.description}\nMessage from Pro: {quote.message}",
        booking_fee=10.00,
        total_amount=float(quote.proposed_price) + 10.00,
        status='pending'
    )
    
    # Update task status
    task.status = 'In Progress'
    task.save()

    # Notify provider
    Notification.objects.create(
        user=quote.provider.user,
        title="🎉 Quote Accepted!",
        message=f"Your quote for '{task.title}' has been accepted by {task.customer.username}. A pending booking has been created.",
        link=reverse('provider_dashboard')
    )
    
    messages.success(request, f"Quote from {quote.provider.business_name} accepted! Please proceed to payment.")
    return redirect('booking_confirm', booking_id=booking.id)
