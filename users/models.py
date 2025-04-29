from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = (
        ('farmer', 'Farmer'),
        ('buyer', 'Buyer'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='farmer')
    
    def is_farmer(self):
        return self.role == 'farmer'

    def is_buyer(self):
        return self.role == 'buyer'

    def is_admin(self):
        return self.role == 'admin'
    
    location = models.CharField(max_length=255)
    lat = models.FloatField(default=0.0)
    lng = models.FloatField(default=0.0)