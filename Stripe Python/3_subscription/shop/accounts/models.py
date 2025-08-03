from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    is_premium  = models.BooleanField(default=False)

    def __str__(self):
        return f'Profile({self.user.username})'

