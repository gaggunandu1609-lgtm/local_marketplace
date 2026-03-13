from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.http import JsonResponse
import requests
from .models import Service, Category, ServiceProvider

def home(request):
    # If a provider is logged in, redirect them to their dashboard
    if request.user.is_authenticated:
        if hasattr(request.user, 'profile') and request.user.profile.role == 'provider':
            return redirect('provider_dashboard')

    city = request.session.get('user_city')
    services = Service.objects.filter(is_active=True)
    
    if city:
        featured_services = services.filter(city__icontains=city)[:6]
        if not featured_services.exists():
            featured_services = services[:6]
    else:
        featured_services = services[:6]
        
    categories = Category.objects.all()
    return render(request, "home.html", {
        "services": featured_services,
        "categories": categories,
        "is_local": bool(city)
    })

def services_view(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    city = request.GET.get('city', '')
    if not city:
        city = request.session.get('user_city', '')
    
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
        request.session['user_city'] = city

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

def detect_city(request):
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    
    if lat and lon:
        try:
            # Use Nominatim for reverse geocoding
            url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&zoom=10&addressdetails=1"
            headers = {'User-Agent': 'LocalMarketplace/1.0'}
            response = requests.get(url, headers=headers, timeout=5)
            data = response.json()
            
            # Extract city from address
            address = data.get('address', {})
            city = (address.get('city') or 
                    address.get('town') or 
                    address.get('suburb') or 
                    address.get('village') or 
                    address.get('city_district') or 
                    address.get('state_district') or 
                    address.get('county'))
            
            if city:
                # Clean up city name
                city = city.split(',')[0].strip()
                
                # Mapping for common variations
                city_mapping = {
                    'Mysuru': 'Mysore',
                    'Bengaluru': 'Bangalore',
                    'Belagavi': 'Belgaum',
                    'Hubballi': 'Hubli',
                    'Kalaburagi': 'Gulbarga',
                    'Shivamogga': 'Shimoga',
                }
                city = city_mapping.get(city, city)
                
                # Verify if this city exists in our DB to ensure a valid selection
                from .models import City
                db_city = City.objects.filter(name__iexact=city).first()
                if db_city:
                    city = db_city.name
                
                request.session['user_city'] = city
                return JsonResponse({'city': city})
        except Exception as e:
            print(f"Error detecting city: {e}")
            
    return JsonResponse({'error': 'Could not detect city'}, status=400)