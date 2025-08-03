from datetime import datetime

import stripe

from django.http import HttpResponse, HttpResponseBadRequest
from django.conf import settings
from django.shortcuts import render, redirect, reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Subscription

stripe.api_key = settings.STRIPE_API_KEY

PRICE_IDS = ['YOUR PRICE ID']


@login_required
def products(request):
    price_objs = [stripe.Price.retrieve(pid) for pid in PRICE_IDS]

    if request.method == 'POST':
        price_id = request.POST.get('price_id')

        checkout_session = stripe.checkout.Session.create(
            line_items = [
                {
                    'price': price_id,
                    'quantity': 1
                }
            ],
            mode = 'subscription',
            success_url=request.build_absolute_uri(reverse("products")) + "?success=1&session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri(reverse("products")) + "?canceled=1",
            client_reference_id=request.user.id  # optional (?)
        )

        return redirect(checkout_session.url, code=303)

    return render(request, 'products/products.html', {'prices': price_objs})


@csrf_exempt
def stripe_webhook(request):
    secret = settings.STRIPE_WEBHOOK_SECRET

    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, secret)
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponseBadRequest()

    event_type = event['type']
    data = event['data']['object']

    if event_type == 'checkout.session.completed':
        sub_id = data['subscription']
        user_id = int(data['client_reference_id'])
        user = User.objects.get(pk=user_id)  # get user based on e-mail

        sub = stripe.Subscription.retrieve(sub_id)
        Subscription.objects.update_or_create(
            user=user,
            stripe_subscription_id=sub_id,
            defaults={
                'status': sub['status'],
                'current_period_end': datetime.fromtimestamp(sub['current_period_end'], tz=timezone.utc) if sub.get('current_period_end') else None
            }
        )

        user.profile.is_premium = True
        user.profile.save()
    elif event_type == 'customer.subscription.updated':
        Subscription.objects.filter(
            stripe_subscription_id=data['id']
        ).update(status=data['status'], current_period_end=datetime.fromtimestamp(data['current_period_end'], tz=timezone.utc) if data.get('current_period_end') else None)
    elif event_type in ('customer.subscription.deleted', 'invoice.payment_failed'):
        try:
            sub = Subscription.objects.get(stripe_subscription_id=data['id'])
        except Subscription.DoesNotExist:
            pass
        else:
            sub.status = 'canceled'
            sub.save()
            sub.user.profile.is_premium = False
            sub.user.profile.save()

    return HttpResponse(status=200)


@login_required
def cancel_subscription(request):
    sub = request.user.subscriptions.filter(status='active').first()
    if not sub:
        return redirect('products')

    stripe.Subscription.modify(sub.stripe_subscription_id, cancel_at_period_end=True)
    return redirect('products')
