from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    booking = models.OneToOneField('bookings.Booking', on_delete=models.CASCADE, related_name="review_details", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    service = models.ForeignKey('services.Service', on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.service.name} by {self.user.username}"
