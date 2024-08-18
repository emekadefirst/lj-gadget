from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from .action import Cart  # Import your Cart model

def order_id():
    now = datetime.now()
    date_str = now.strftime('%Y%m%d')
    time_str = now.strftime('%H%M%S')
    return f'OD{date_str}{time_str}'

class Order(models.Model):
    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('en_route', 'En Route'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    id = models.AutoField(primary_key=True)
    order_code = models.CharField(max_length=15, default=order_id, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Cart)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='processing')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Order {self.order_code} - {self.user.username}"
    

    
class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)