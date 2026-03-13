from services.models import City

def user_location(request):
    """
    Context processor to make the user's selected or detected city 
    and list of available cities available in all templates.
    """
    current_city = request.session.get('user_city')
    
    # If not in session, try to get from query param (but session is better for persistence)
    if not current_city:
        current_city = request.GET.get('city')
        if current_city:
            request.session['user_city'] = current_city
            
    # Default city if none found
    return {
        'current_city': current_city or "Mumbai",
        'db_cities': list(City.objects.all().order_by('name'))
    }
