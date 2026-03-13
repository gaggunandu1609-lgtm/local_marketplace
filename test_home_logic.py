import os
import django
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'local_marketplace.settings')
django.setup()

from services.views import home
from services.models import Service, City

def test_home_view():
    factory = RequestFactory()
    request = factory.get('/')
    
    # Manually add session
    middleware = SessionMiddleware(lambda r: None)
    middleware.process_request(request)
    request.session.save()
    
    # Case 1: No city in session
    response = home(request)
    print(f"Home view without city in session: {len(response.context_data['services'])} services shown")
    
    # Case 2: City in session (e.g., Mysore)
    request.session['user_city'] = 'Mysore'
    response = home(request)
    services = response.context_data['services']
    print(f"Home view with Mysore in session: {len(services)} services shown")
    for s in services:
        print(f"  Service: {s.name} in {s.city}")

if __name__ == '__main__':
    test_home_view()
