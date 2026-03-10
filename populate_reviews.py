import os
import django
import random
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'local_marketplace.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import Profile
from services.models import Service
from reviews.models import Review

# 1. Create more customer users if needed
def ensure_customers():
    customer_names = [
        "Amit", "Priya", "Sunita", "Rajesh", "Anjali", 
        "Vikram", "Neha", "Suresh", "Kavita", "Rahul",
        "Pooja", "Arjun", "Sneha", "Manoj", "Deepika"
    ]
    print(f"Ensuring at least {len(customer_names)} customers...")
    for name in customer_names:
        username = name.lower() + "_cust"
        user, created = User.objects.get_or_create(username=username, defaults={'email': f"{username}@example.com"})
        if created:
            user.set_password('pass123')
            user.save()
            Profile.objects.get_or_create(user=user, defaults={'role': 'customer'})
    print("Customers ensured.")

# 2. Sample Review Comments
REVIEW_TEMPLATES = {
    5: [
        "Excellent service! Highly recommended.",
        "Very professional and punctual. Fixed everything quickly.",
        "Great experience! The quality of work exceeded my expectations.",
        "Friendly and expert service. Will definitely book again.",
        "Super happy with the results. Value for money!"
    ],
    4: [
        "Good work, but arrived a bit late.",
        "The job was done well. Satisfied with the results.",
        "Reliable service and fair pricing.",
        "Professional behavior. Quality of materials used was good.",
        "Overall a good experience. A bit room for improvement in cleanup."
    ],
    3: [
        "Average service. Could be better.",
        "Fixed the issue but it took much longer than expected.",
        "Pricing was okay, but the worker was a bit unprofessional.",
        "The work is fine, nothing special.",
        "Satisfied but not fully. Needs to improve communication."
    ]
}

def populate_reviews():
    ensure_customers()
    
    customers = list(User.objects.filter(profile__role='customer'))
    services = Service.objects.all()
    
    print(f"Starting review population for {services.count()} services...")
    
    # Clean existing reviews if needed? Maybe better to just add to them.
    # Review.objects.all().delete()
    
    for service in services:
        # Each service gets 1-3 reviews
        num_reviews = random.randint(1, 3)
        
        # Decide average rating based on the provider's current rating if possible
        target_avg = service.provider.rating if service.provider.rating > 0 else 4.5
        
        for _ in range(num_reviews):
            customer = random.choice(customers)
            
            # Generate a rating around the target average
            if target_avg >= 4.5:
                rating = random.choices([5, 4, 3], weights=[70, 20, 10])[0]
            elif target_avg >= 3.5:
                rating = random.choices([5, 4, 3], weights=[30, 50, 20])[0]
            else:
                rating = random.choices([4, 3, 2], weights=[20, 50, 30])[0]
            
            comment = random.choice(REVIEW_TEMPLATES.get(rating, REVIEW_TEMPLATES[5]))
            
            # Create the review
            Review.objects.create(
                user=customer,
                service=service,
                rating=rating,
                comment=comment
            )
        
        print(f"  Added {num_reviews} reviews for: {service.name}")

if __name__ == "__main__":
    populate_reviews()
    print("\nReview population complete.")
