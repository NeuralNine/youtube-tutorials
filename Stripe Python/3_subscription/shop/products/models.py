from django.db import models
from django.conf import settings


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    stripe_subscription_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=32, default='active')  # active | past_due | canceled | unpaid
    current_period_end = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

