import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'local_marketplace.settings')
django.setup()

from services.models import ServiceProvider, City, Service, Category

def check_data():
    print(f"Total Cities: {City.objects.count()}")
    print(f"Total Providers: {ServiceProvider.objects.count()}")
    print(f"Total Services: {Service.objects.count()}")
    print(f"Total Categories: {Category.objects.count()}")
    
    print("\nCities Sample:")
    for city in City.objects.all()[:10]:
        print(f"- {city.name}, {city.state}")
        
    print("\nRecent Services Sample:")
    for service in Service.objects.all().order_by('-id')[:5]:
        print(f"- {service.name} in {service.city} by {service.provider.business_name} (Price: {service.price})")

if __name__ == '__main__':
    check_data()
