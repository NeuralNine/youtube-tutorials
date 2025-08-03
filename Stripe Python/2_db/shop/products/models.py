from django.db import models
from django.conf import settings


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    stripe_session_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

