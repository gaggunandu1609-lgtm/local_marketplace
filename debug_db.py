import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'local_marketplace.settings')
django.setup()

from services.models import Service, ServiceProvider, Category

print("--- RECENT SERVICES ---")
for s in Service.objects.all().order_by('-id')[:5]:
    print(f"ID: {s.id}, Name: {s.name}, Provider: {s.provider.business_name}, Category: {s.category.name if s.category else 'N/A'}, City: {s.city}, Active: {s.is_active}")

print("\n--- RECENT PROVIDERS ---")
for p in ServiceProvider.objects.all().order_by('-id')[:5]:
    print(f"ID: {p.id}, Business: {p.business_name}, Category: {p.category.name if p.category else 'N/A'}, City: {p.city_ref.name if p.city_ref else 'N/A'}")

print("\n--- CATEGORIES ---")
for c in Category.objects.all():
    print(f"ID: {c.id}, Name: {c.name}")
