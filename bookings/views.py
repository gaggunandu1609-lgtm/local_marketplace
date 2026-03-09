import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from .models import Booking
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


def payment_success(request):
    return render(request, "payment_success.html")


def payment_cancel(request):
    return render(request, "payment_cancel.html")



def create_checkout_session(request, booking_id):
    booking = Booking.objects.get(id=booking_id)

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'inr',
                'product_data': {
                    'name': f"Service by {booking.provider.full_name}",
                },
                'unit_amount': int(booking.amount * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('payment_success')) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=request.build_absolute_uri(reverse('payment_cancel')),
    )

    return redirect(checkout_session.url, code=303)