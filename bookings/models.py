from django.db import models
from django.contrib.auth.models import User
from services.models import ServiceProvider

class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed'),
    ]

    customer = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name="marketplace_bookings"
)
    service = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.username} - {self.service.title}"