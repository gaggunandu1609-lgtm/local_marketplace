import os
import django
import sys

# Setup Django environment
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'local_marketplace.settings')
django.setup()

from services.models import Service, ServiceProvider, PortfolioImage, Category

# Map exact category names from CSV to image paths in media/services/
IMAGE_MAPPING = {
    'Plumber': 'services/plumbing.jpg',
    'Electrician': 'services/electrical.jpg',
    'Home Cleaner': 'services/cleaning.jpg',
    'Carpenter': 'services/carpentry.jpg',
    'Painting': 'services/painting.jpg',
    'AC Repair Technician': 'services/appliance.jpg',
    'Laptop/Computer Repair': 'services/appliance.jpg', # Using appliance as fallback
    'Bike Mechanic': 'services/appliance.jpg', # Using appliance as fallback
    'Photographer': 'services/painting.jpg', # Using painting as fallback
    'Beautician (Home Service)': 'services/cleaning.jpg', # Using cleaning as fallback
    'Home Tutor': 'services/carpentry.jpg', # Using carpentry as fallback
}

def populate():
    print("Updating service images based on exact CSV categories...")
    services = Service.objects.all()
    for service in services:
        cat_name = service.category.name if service.category else 'Plumber'
        image_path = IMAGE_MAPPING.get(cat_name, 'services/plumbing.jpg')
        service.image = image_path
        service.save()
        print(f"  Updated image for: {service.name} (Category: {cat_name})")

    print("\nUpdating portfolio images for all providers...")
    # Clean up existing portfolio images if any to refresh
    PortfolioImage.objects.all().delete()
    
    providers = ServiceProvider.objects.all()
    # Available actual files for portfolio
    portfolio_files = ['portfolio/p2.jpg', 'portfolio/p3.jpg', 'services/plumbing.jpg', 'services/electrical.jpg', 'services/cleaning.jpg']
    
    for provider in providers:
        # Assign 4 sample portfolio images to each provider
        for i in range(4):
            file_path = portfolio_files[i % len(portfolio_files)]
            PortfolioImage.objects.create(
                provider=provider,
                image=file_path,
                caption=f"Completed work by {provider.business_name}"
            )
        print(f"  Added 4 portfolio photos for: {provider.business_name}")

if __name__ == "__main__":
    populate()
    print("\nData update complete.")
