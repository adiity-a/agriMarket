from django.db import models
from products.models import Product
from users.models import User
from django.utils import timezone
from datetime import timedelta

class Bid(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    offered_price = models.FloatField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return (timezone.now() - self.timestamp) > timedelta(days=10)

