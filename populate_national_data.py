import os
import random
import django
import sys
from datetime import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'local_marketplace.settings')
django.setup()

from services.models import ServiceProvider, City, Category, Service
from django.contrib.auth.models import User
from accounts.models import Profile

INDIA_CITIES = {
    'Karnataka': ['Bangalore', 'Mysore', 'Hubli', 'Mangalore', 'Belgaum', 'Davanagere', 'Gulbarga', 'Bellary'],
    'Maharashtra': ['Mumbai', 'Pune', 'Nagpur', 'Nashik', 'Thane', 'Aurangabad', 'Solapur'],
    'Tamil Nadu': ['Chennai', 'Coimbatore', 'Madurai', 'Trichy', 'Salem', 'Tirunelveli'],
    'Telangana': ['Hyderabad', 'Warangal', 'Nizamabad', 'Khammam', 'Karimnagar'],
    'Delhi': ['New Delhi', 'Noida', 'Gurgaon', 'Faridabad'],
    'West Bengal': ['Kolkata', 'Howrah', 'Durgapur', 'Asansol', 'Siliguri'],
    'Gujarat': ['Ahmedabad', 'Surat', 'Vadodara', 'Rajkot', 'Bhavnagar'],
    'Rajasthan': ['Jaipur', 'Jodhpur', 'Udaipur', 'Kota', 'Ajmer'],
    'Uttar Pradesh': ['Lucknow', 'Kanpur', 'Varanasi', 'Agra', 'Ghaziabad', 'Meerut', 'Prayagraj'],
    'Kerala': ['Kochi', 'Thiruvananthapuram', 'Kozhikode', 'Thrissur', 'Kollam'],
    'Punjab': ['Ludhiana', 'Amritsar', 'Jalandhar', 'Patiala', 'Bathinda'],
    'Madhya Pradesh': ['Indore', 'Bhopal', 'Gwalior', 'Jabalpur', 'Ujjain'],
    'Andhra Pradesh': ['Visakhapatnam', 'Vijayawada', 'Guntur', 'Nellore', 'Kurnool'],
    'Bihar': ['Patna', 'Gaya', 'Bhagalpur', 'Muzaffarpur', 'Purnia'],
    'Haryana': ['Chandigarh', 'Ambala', 'Panipat', 'Karnal'],
    'Odisha': ['Bhubaneswar', 'Cuttack', 'Rourkela', 'Brahmapur'],
    'Assam': ['Guwahati', 'Dibrugarh', 'Silchar', 'Jorhat'],
}

CATEGORIES = [
    ('Photographer', 'fa-camera'),
    ('Bike Mechanic', 'fa-motorcycle'),
    ('Electrician', 'fa-bolt'),
    ('Carpenter', 'fa-hammer'),
    ('AC Repair Technician', 'fa-snowflake'),
    ('Beautician (Home Service)', 'fa-magic'),
    ('Laptop/Computer Repair', 'fa-laptop'),
    ('Plumber', 'fa-faucet'),
    ('Home Tutor', 'fa-book'),
    ('Home Cleaner', 'fa-broom'),
    ('Painter', 'fa-paint-roller'),
    ('Pest Control', 'fa-bug'),
    ('Gardener', 'fa-leaf'),
    ('Appliance Repair', 'fa-tv')
]

FIRST_NAMES = ['Aditya', 'Vikram', 'Rahul', 'Deepak', 'Arjun', 'Rohan', 'Vijay', 'Suresh', 'Varun', 'Karan', 
               'Neha', 'Priya', 'Ananya', 'Simran', 'Kavya', 'Sana', 'Zoya', 'Sneha', 'Sunita', 'Anita',
               'Amit', 'Rajesh', 'Sanjay', 'Manoj', 'Pankaj', 'Sachin', 'Pooja', 'Megha', 'Ritu', 'Kajal']

LAST_NAMES = ['Sharma', 'Verma', 'Gupta', 'Singh', 'Kumar', 'Yadav', 'Patel', 'Reddy', 'Nair', 'Chavan',
              'Iyer', 'Bannerjee', 'Dutta', 'Mishra', 'Joshi', 'Kulkarni', 'Deshmukh', 'Rao', 'Reddy', 'Gill']

BUSINESS_SUFFIXES = ['Services', 'Solutions', 'Care', 'Expert', 'Center', 'Studio', 'Hub', 'Fix', 'Pro', 'Tech']

def get_random_lat_lon(city_name):
    # Dummy central lat/lon for some cities to keep things simple
    city_coords = {
        'Mumbai': (19.0760, 72.8777),
        'Delhi': (28.6139, 77.2090),
        'Bangalore': (12.9716, 77.5946),
        'Hyderabad': (17.3850, 78.4867),
        'Ahmedabad': (23.0225, 72.5714),
        'Chennai': (13.0827, 80.2707),
        'Kolkata': (22.5726, 88.3639),
        'Pune': (18.5204, 73.8567),
        'Jaipur': (26.9124, 75.7873),
        'Lucknow': (26.8467, 80.9462),
        'Mysore': (12.2958, 76.6394),
    }
    
    base = city_coords.get(city_name, (20.5937, 78.9629)) # India center
    return (base[0] + random.uniform(-0.1, 0.1), base[1] + random.uniform(-0.1, 0.1))

def run(count=200):
    print(f"Generating {count} providers across India...")
    
    # Ensure categories exist
    cat_objs = {}
    for cat_name, icon in CATEGORIES:
        cat, _ = Category.objects.get_or_create(name=cat_name, defaults={'icon': icon})
        cat_objs[cat_name] = cat
    
    # Get all existing users to avoid clashes if needed, but we'll use unique usernames
    
    for i in range(count):
        state = random.choice(list(INDIA_CITIES.keys()))
        city_name = random.choice(INDIA_CITIES[state])
        
        city_obj, _ = City.objects.get_or_create(name=city_name, defaults={'state': state})
        
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        full_name = f"{first_name} {last_name}"
        
        # Unique username
        username = f"provider_{state.lower()[:3]}_{city_name.lower()[:3]}_{i}"
        user, created = User.objects.get_or_create(
            username=username, 
            defaults={
                'email': f"{username}@example.com",
                'first_name': first_name,
                'last_name': last_name
            }
        )
        if created:
            user.set_password('pass123')
            user.save()
        
        Profile.objects.get_or_create(user=user, defaults={'role': 'provider'})
        
        cat_name, _ = random.choice(CATEGORIES)
        category = cat_objs[cat_name]
        
        suffix = random.choice(BUSINESS_SUFFIXES)
        business_name = f"{full_name} {cat_name} {suffix}"
        
        lat, lon = get_random_lat_lon(city_name)
        
        provider, _ = ServiceProvider.objects.update_or_create(
            user=user,
            defaults={
                'business_name': business_name,
                'description': f"Top rated {cat_name.lower()} expert providing high quality services in {city_name} and surrounding areas.",
                'phone_number': f"{random.randint(7000, 9999)}{random.randint(100000, 999999)}",
                'city_ref': city_obj,
                'area': "Main City Area",
                'latitude': lat,
                'longitude': lon,
                'experience_years': random.randint(1, 20),
                'rating': round(random.uniform(3.5, 5.0), 1),
                'total_jobs': random.randint(5, 500),
                'verified': random.choice([True, False, True]), # Bias towards verified
                'availability': random.choice(['Available', 'Available', 'Busy'])
            }
        )
        
        # Create the service
        Service.objects.update_or_create(
            provider=provider,
            category=category,
            name=f"{cat_name} Expert Service",
            defaults={
                'description': f"Get professional {cat_name.lower()} services from {business_name}. We guarantee satisfaction and competitive pricing.",
                'price': float(random.randint(300, 5000)),
                'is_active': True,
                'city': city_name,
                'area': "Main City Area"
            }
        )
        
        if i % 20 == 0:
            print(f"Processed {i} providers...")

if __name__ == '__main__':
    run(250)
    print("National data generation completed!")
