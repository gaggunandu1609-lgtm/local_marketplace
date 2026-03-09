import csv
import os
import django
import sys
from datetime import datetime

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'intern_project.settings')
django.setup()

from services.models import ServiceProvider

def run():
    csv_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'services_data.csv')
    
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            provider_id = row['provider_id']
            # Check if this provider already exists
            if not ServiceProvider.objects.filter(provider_id=provider_id).exists():
                ServiceProvider.objects.create(
                    provider_id=provider_id,
                    full_name=row['full_name'],
                    service_category=row['service_category'],
                    phone_number=row['phone_number'],
                    city=row['city'],
                    area=row['area'],
                    experience_year=int(row['experience_years']),
                    starting_price=float(row['starting_price']),
                    rating=float(row['rating']),
                    total_jobs=int(row['total_jobs']),
                    availability_status=(row['availability_status'].lower() == 'available'),
                    verified=(row['verified'].lower() == 'yes'),
                    registration_date=datetime.strptime(row['registration_date'], '%Y-%m-%d').date()
                )
                print(f"Created provider: {row['full_name']}")
            else:
                print(f"Provider {provider_id} already exists. Skipping.")

if __name__ == '__main__':
    print("Loading data...")
    run()
    print("Data loading completed!")
