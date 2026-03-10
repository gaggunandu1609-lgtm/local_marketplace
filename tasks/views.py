from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task, Quote
from services.models import City, ServiceProvider
from django.contrib import messages

@login_required
def post_task(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        budget = request.POST.get('budget')
        city_id = request.POST.get('city')
        location_details = request.POST.get('location_details')
        preferred_date = request.POST.get('preferred_date')
        
        Task.objects.create(
            customer=request.user,
            title=title,
            description=description,
            budget=budget,
            city_ref_id=city_id,
            location_details=location_details,
            preferred_date=preferred_date,
            status='Open'
        )
        messages.success(request, "Your task has been posted successfully!")
        return redirect('my_tasks')
        
    cities = City.objects.all()
    return render(request, "tasks/post_task.html", {"cities": cities})

@login_required
def task_list(request):
    # For providers to see open tasks in their city
    try:
        provider = request.user.provider_profile
        tasks = Task.objects.filter(status='Open', city_ref=provider.city_ref).order_by('-created_at')
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
        
        Quote.objects.create(
            task=task,
            provider=request.user.provider_profile,
            proposed_price=proposed_price,
            message=message
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
