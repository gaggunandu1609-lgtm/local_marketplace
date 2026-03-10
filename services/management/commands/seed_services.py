import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from services.models import Category, ServiceProvider, Service

class Command(BaseCommand):
    help = 'Seed the database with sample services, categories, and providers'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # 1. Create Categories
        categories_data = [
            {'name': 'Plumbing', 'icon': 'fa-faucet'},
            {'name': 'Electrical', 'icon': 'fa-bolt'},
            {'name': 'Cleaning', 'icon': 'fa-broom'},
            {'name': 'Gardening', 'icon': 'fa-leaf'},
            {'name': 'Carpentry', 'icon': 'fa-hammer'},
        ]
        
        categories = []
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(name=cat_data['name'], defaults={'icon': cat_data['icon']})
            categories.append(cat)
            if created:
                self.stdout.write(f'Created category: {cat.name}')

        # 2. Create Sample Providers & Services
        providers_info = [
            {
                'username': 'plumber_pro',
                'business_name': 'Elite Plumbing Solutions',
                'services': [
                    {'name': 'Pipe Leak Repair', 'price': 500, 'desc': 'Professional repair of all pipe leaks.'},
                    {'name': 'Drain Cleaning', 'price': 800, 'desc': 'Unclogging and cleaning drains.'}
                ]
            },
            {
                'username': 'electric_wizard',
                'business_name': 'VoltMaster Electrical',
                'services': [
                    {'name': 'Wiring Installation', 'price': 1500, 'desc': 'Complete house wiring services.'},
                    {'name': 'Switchboard Repair', 'price': 300, 'desc': 'Fixing faulty switchboards and sockets.'}
                ]
            },
            {
                'username': 'clean_queen',
                'business_name': 'Sparkle & Shine Cleaning',
                'services': [
                    {'name': 'Deep Home Cleaning', 'price': 2500, 'desc': 'Full house deep cleaning service.'},
                    {'name': 'Sofa Shampooing', 'price': 1200, 'desc': 'Deep cleaning for your expensive sofas.'}
                ]
            }
        ]

        for p_info in providers_info:
            user, created = User.objects.get_or_create(
                username=p_info['username'],
                defaults={'email': f"{p_info['username']}@example.com"}
            )
            if created:
                user.set_password('password123')
                user.save()

            provider, created = ServiceProvider.objects.get_or_create(
                user=user,
                defaults={
                    'business_name': p_info['business_name'],
                    'description': f"Experienced {p_info['business_name']} provider.",
                    'phone_number': '1234567890',
                    'city': 'Sample City',
                    'area': 'Sample Area',
                    'rating': round(random.uniform(4.0, 5.0), 1),
                    'total_jobs': random.randint(10, 100),
                    'verified': True
                }
            )

            for s_data in p_info['services']:
                cat = random.choice(categories)
                # Try to match category name if possible
                for c in categories:
                    if c.name.lower() in s_data['name'].lower() or c.name.lower() in p_info['business_name'].lower():
                        cat = c
                        break
                
                service, created = Service.objects.get_or_create(
                    provider=provider,
                    name=s_data['name'],
                    defaults={
                        'category': cat,
                        'description': s_data['desc'],
                        'price': s_data['price'],
                        'is_active': True
                    }
                )
                if created:
                    self.stdout.write(f'Created service: {service.name} for {provider.business_name}')

        self.stdout.write(self.style.SUCCESS('Successfully seeded database!'))
