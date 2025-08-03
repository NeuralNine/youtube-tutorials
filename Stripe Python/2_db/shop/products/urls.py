from django.urls import path
from .views import products, stripe_webhook

urlpatterns = [
    path('', products, name='products'),
    path('stripe/webhook', stripe_webhook, name='stripe-webhook')
]
