import csv
import os
import django
import sys
import random
from datetime import datetime

# Setup Django environment
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'local_marketplace.settings')
django.setup()

from services.models import ServiceProvider, City, Category, Service
from django.contrib.auth.models import User
from accounts.models import Profile

def run():
    csv_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'services_data.csv')
    
    # Base location for Pune (for distance testing)
    BASE_LAT = 18.5204
    BASE_LON = 73.8567

    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            provider_id = row['provider_id']
            # We use username based on provider_id for uniqueness
            username = f"provider_{provider_id}"
            
            # 1. Ensure User exists
            user, created = User.objects.get_or_create(username=username, defaults={'email': f"{username}@example.com"})
            if created:
                user.set_password('pass123')
                user.save()
            
            # 2. Ensure Profile exists
            profile, _ = Profile.objects.get_or_create(user=user, defaults={'role': 'provider'})
            
            # 3. Ensure Category exists
            cat_name = row['service_category']
            category, _ = Category.objects.get_or_create(name=cat_name)

            # 4. Ensure City exists
            city_name = row['city']
            city_obj, _ = City.objects.get_or_create(name=city_name, defaults={'state': 'State'})

            # 5. Create/Update ServiceProvider
            business_name = row['full_name']
            
            lat = float(row.get('latitude', BASE_LAT + random.uniform(-0.15, 0.15)))
            lon = float(row.get('longitude', BASE_LON + random.uniform(-0.15, 0.15)))

            provider, _ = ServiceProvider.objects.update_or_create(
                user=user,
                defaults={
                    'business_name': business_name,
                    'description': f"Expert {cat_name} services in {row['area']}, {city_name}.",
                    'phone_number': row['phone_number'],
                    'city_ref': city_obj,
                    'area': row['area'],
                    'latitude': lat,
                    'longitude': lon,
                    'experience_years': int(row['experience_years']),
                    'rating': float(row['rating']),
                    'total_jobs': int(row['total_jobs']),
                    'verified': (row['verified'].lower() == 'yes'),
                    'availability': 'Available' if row['availability_status'].lower() == 'available' else 'Busy'
                }
            )
            
            # 6. Create a default Service entry for this provider
            Service.objects.update_or_create(
                provider=provider,
                category=category,
                name=f"{cat_name} Service",
                defaults={
                    'description': f"Professional {cat_name.lower()} service by {business_name}.",
                    'price': float(row['starting_price']),
                    'is_active': True,
                    'city': city_name,
                    'area': row['area']
                }
            )

            print(f"Loaded provider: {business_name} ({cat_name})")

if __name__ == '__main__':
    print("Loading realistic data from CSV...")
    run()
    print("Data loading completed!")
