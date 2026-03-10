from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posted_tasks")
    title = models.CharField(max_length=200)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    city_ref = models.ForeignKey('services.City', on_delete=models.SET_NULL, null=True, related_name='tasks')
    location_details = models.CharField(max_length=255, help_text="Specific area or address")
    preferred_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Quote(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="quotes")
    provider = models.ForeignKey('services.ServiceProvider', on_delete=models.CASCADE, related_name="sent_quotes")
    proposed_price = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Quote from {self.provider.business_name} for {self.task.title}"
