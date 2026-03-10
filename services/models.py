from django.db import models
from django.contrib.auth.models import User

class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}, {self.state}"

    class Meta:
        verbose_name_plural = "Cities"

class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True, help_text="FontAwesome icon class")
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class ServiceProvider(models.Model):
    AVAILABILITY_CHOICES = [
        ('Available', 'Available'),
        ('Busy', 'Busy'),
        ('Offline', 'Offline'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='provider_profile')
    business_name = models.CharField(max_length=200)
    profile_photo = models.ImageField(upload_to='providers/', blank=True, null=True)
    description = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20)
    city_ref = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_name='providers')
    area = models.CharField(max_length=100)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    experience_years = models.IntegerField(default=0)
    rating = models.FloatField(default=0.0)
    total_jobs = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='Available')
    registration_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.business_name

class PortfolioImage(models.Model):
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='portfolio_images')
    image = models.ImageField(upload_to='portfolio/')
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Portfolio for {self.provider.business_name}"

class Service(models.Model):
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='services')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='services')
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    city = models.CharField(max_length=100, blank=True)
    area = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def average_rating(self):
        from reviews.models import Review
        # Get reviews for this service
        reviews = Review.objects.filter(service=self)
        if reviews.exists():
            import django.db.models as db_models
            return reviews.aggregate(db_models.Avg('rating'))['rating__avg']
        return 0.0

    def total_reviews(self):
        from reviews.models import Review
        return Review.objects.filter(service=self).count()

    def __str__(self):
        return self.name

class ServiceImage(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='services/gallery/')
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Image for {self.service.name}"