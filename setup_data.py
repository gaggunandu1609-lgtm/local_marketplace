import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'local_marketplace.settings')
django.setup()

from services.models import Category

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
    print(f"Ensured category: {name}")
