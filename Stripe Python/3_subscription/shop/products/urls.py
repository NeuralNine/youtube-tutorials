from django.urls import path
from .views import products, stripe_webhook, cancel_subscription

urlpatterns = [
    path('', products, name='products'),
    path('cancel/', cancel_subscription, name='cancel'),
    path('stripe/webhook', stripe_webhook, name='stripe-webhook')
]
