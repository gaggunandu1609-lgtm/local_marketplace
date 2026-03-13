from django.db import models
from django.contrib.auth.models import User

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('in progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('pending payment', 'Pending Payment'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    service = models.ForeignKey('services.Service', on_delete=models.CASCADE, related_name="bookings")
    provider = models.ForeignKey('services.ServiceProvider', on_delete=models.CASCADE, related_name="provider_bookings", null=True, blank=True)
    task = models.ForeignKey('tasks.Task', on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    booking_date = models.DateField()
    booking_time = models.TimeField(null=True, blank=True)
    address = models.TextField(blank=True, default='')
    description = models.TextField(blank=True)
    booking_fee = models.DecimalField(max_digits=10, decimal_places=2, default=10.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, default='online')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.service.name} - {self.status}"