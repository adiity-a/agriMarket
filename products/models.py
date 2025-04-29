from django.db import models
from users.models import User

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    quantity = models.IntegerField()
    farmer = models.ForeignKey(User, on_delete=models.CASCADE)
    lat = models.FloatField()
    lng = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
