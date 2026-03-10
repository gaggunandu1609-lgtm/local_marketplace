from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Service, Category, ServiceProvider

def home(request):
    featured_services = Service.objects.filter(is_active=True)[:6]
    categories = Category.objects.all()
    return render(request, "home.html", {
        "services": featured_services,
        "categories": categories
    })

def services_view(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    city = request.GET.get('city', '')
    sort_by = request.GET.get('sort', 'newest')
    
    services = Service.objects.filter(is_active=True)

    if query:
        services = services.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(provider__business_name__icontains=query)
        )
    
    if category_id:
        services = services.filter(category_id=category_id)
        
    if city:
        services = services.filter(city__icontains=city)

    # Sorting
    if sort_by == 'price_low':
        services = services.order_by('price')
    elif sort_by == 'price_high':
        services = services.order_by('-price')
    elif sort_by == 'newest':
        services = services.order_by('-created_at')
    else: # default rating
        services = services.order_by('-provider__rating')

    categories = Category.objects.all()

    context = {
        "services": services,
        "categories": categories,
        "query": query,
        "selected_category": category_id,
        "selected_city": city,
        "sort_by": sort_by,
    }
    
    if request.htmx:
        return render(request, "services/_service_list.html", context)
        
    return render(request, "services.html", context)

def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    reviews = service.reviews.all().order_by('-created_at')
    # Get other services from the same provider
    related_services = Service.objects.filter(provider=service.provider).exclude(id=service.id)[:4]
    
    return render(request, "service_details.html", {
        "service": service,
        "reviews": reviews,
        "related_services": related_services
    })