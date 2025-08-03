import os

import stripe
from flask import Flask, request, render_template, redirect, url_for
from dotenv import load_dotenv

load_dotenv()
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():

    print(url_for('success') + '?session_id={CHECKOUT_SESSION_ID}')

    if request.method == 'POST':
        price_id = 'YOUR PRICE ID'  # not product id

        price_obj = stripe.Price.retrieve(price_id)
        unit_amount = price_obj.unit_amount

        checkout_session = stripe.checkout.Session.create(
            line_items = [
                {
                    'price': price_id,
                    'quantity': 1
                }
            ],
            mode = 'payment',
            success_url = url_for('success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url = url_for('cancel', _external=True)
        )

        return redirect(checkout_session.url, code=303)
    else:
        return render_template('index.html')


@app.route('/success')
def success():
    session_id = request.args.get('session_id')
    session = stripe.checkout.Session.retrieve(session_id)

    if session.payment_status == 'paid':
        return f'Successfully purchased! (Session ID: {session_id}, Status: {session.payment_status})'
    else:
        return redirect(url_for('cancel'))


@app.route('/cancel')
def cancel():
    return 'Payment canceled!'


if __name__ == '__main__':
    app.run()

