import stripe

from django.http import HttpResponse, HttpResponseBadRequest
from django.conf import settings
from django.shortcuts import render, redirect, reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import Order

stripe.api_key = settings.STRIPE_API_KEY

PRICE_IDS = ['YOUR PRICE ID']


@login_required
def products(request):
    price_objs = [stripe.Price.retrieve(pid) for pid in PRICE_IDS]

    if request.method == 'POST':
        price_id = request.POST.get('price_id')

        order = Order.objects.create(
            user = request.user,
            stripe_session_id = '',
            amount = 1,
            paid = False
        )

        checkout_session = stripe.checkout.Session.create(
            line_items = [
                {
                    'price': price_id,
                    'quantity': 1
                }
            ],
            mode = 'payment',
            success_url=request.build_absolute_uri(reverse("products")) + "?success=1&session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri(reverse("products")) + "?canceled=1",
            metadata={'order_id': order.pk}
        )

        order.stripe_session_id = checkout_session.id
        order.amount = checkout_session.amount_total
        order.save()

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

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        order_id = session['metadata'].get('order_id')

        Order.objects.filter(pk=order_id, paid=False).update(paid=True)

    return HttpResponse(status=200)

