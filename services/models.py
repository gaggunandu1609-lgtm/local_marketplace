from django.db import models

class ServiceProvider(models.Model):
    provider_id = models.CharField(max_length=50)
    full_name = models.CharField(max_length=200)
    service_category = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    experience_year = models.IntegerField()
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()
    total_jobs = models.IntegerField()
    availability_status = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)
    registration_date = models.DateField()

    def __str__(self):
        return self.full_name