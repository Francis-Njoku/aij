from django.db import models
#from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from authentication.models import User
# Create your models here.

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="USD")
    stripe_payment_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=50, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} {self.currency} - {self.status}"
    
    
class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=255)
    trial_end_date = models.DateTimeField()
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    status = models.CharField(max_length=20)  # e.g., "active", "inactive", "cancelled"
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {'Active' if self.is_active else 'Inactive'}"
    
class PaymentHistory(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    stripe_payment_id = models.CharField(max_length=255)

    def __str__(self):
        return f"Payment on {self.payment_date} for {self.subscription.user.username}"