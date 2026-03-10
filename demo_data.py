import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'local_marketplace.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import Profile
from services.models import ServiceProvider, Service, Category

# 1. Ensure Categories
CATEGORIES = [
    ('Plumbing', 'fa-solid fa-faucet-detergent'),
    ('Electrician', 'fa-solid fa-bolt'),
    ('Cleaning', 'fa-solid fa-broom'),
    ('Carpentry', 'fa-solid fa-hammer'),
    ('Painting', 'fa-solid fa-paint-roller'),
    ('Appliance Repair', 'fa-solid fa-plug'),
]

for name, icon in CATEGORIES:
    Category.objects.get_or_create(name=name, defaults={'icon': icon})

print("Categories ensured.")

# 2. Create Providers
PROVIDERS_DATA = [
    {
        'username': 'provider1',
        'email': 'pro1@example.com',
        'biz_name': 'Expert Plumbing Solutions',
        'city': 'Mumbai',
        'services': [
            {'cat': 'Plumbing', 'name': 'Full House Leak Inspection', 'price': 1200},
            {'cat': 'Plumbing', 'name': 'Kitchen Sink Repair', 'price': 500},
        ]
    },
    {
        'username': 'provider2',
        'email': 'pro2@example.com',
        'biz_name': 'Voltage Pros Electrical',
        'city': 'Delhi',
        'services': [
            {'cat': 'Electrician', 'name': 'Short Circuit Troubleshooting', 'price': 800},
            {'cat': 'Electrician', 'name': 'Ceiling Fan Installation', 'price': 300},
        ]
    },
    {
        'username': 'provider3',
        'email': 'pro3@example.com',
        'biz_name': 'Sparkle & Shine Cleaning',
        'city': 'Bangalore',
        'services': [
            {'cat': 'Cleaning', 'name': '3BHK Deep Cleaning', 'price': 4500},
            {'cat': 'Cleaning', 'name': 'Sofa & Carpet Shampooing', 'price': 1500},
        ]
    }
]

for p_data in PROVIDERS_DATA:
    if not User.objects.filter(username=p_data['username']).exists():
        u = User.objects.create_user(p_data['username'], p_data['email'], 'pass123')
        p, _ = Profile.objects.get_or_create(user=u)
        p.role = 'provider'
        p.save()
        
        sp = ServiceProvider.objects.create(
            user=u,
            business_name=p_data['biz_name'],
            description=f"Professional services in {p_data['city']}.",
            experience_years=10,
            city=p_data['city'],
            area='Main',
            verified=True
        )
        print(f"Created provider: {p_data['username']}")
        
        for s_info in p_data['services']:
            cat = Category.objects.get(name=s_info['cat'])
            Service.objects.create(
                provider=sp,
                category=cat,
                name=s_info['name'],
                description=f"High-quality {s_info['name'].lower()} service.",
                price=s_info['price'],
                is_active=True
            )
            print(f"  Added service: {s_info['name']}")

# 3. Create Customer
if not User.objects.filter(username='customer1').exists():
    u = User.objects.create_user('customer1', 'cust1@example.com', 'pass123')
    p, _ = Profile.objects.get_or_create(user=u)
    p.role = 'customer'
    p.save()
    print("Created customer: customer1")

print("Demo data population complete.")
