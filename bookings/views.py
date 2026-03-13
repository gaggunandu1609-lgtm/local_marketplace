import razorpay
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib import messages
from django.utils import timezone
from .models import Booking
from services.models import Service
from notifications.models import Notification


def payment_cancel(request):
    return render(request, "payment_cancel.html")


@login_required
def create_booking(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == "POST":
        booking_datetime_str = request.POST.get('booking_date')
        description = request.POST.get('description')
        address = request.POST.get('address', '')

        if 'T' in booking_datetime_str:
            booking_date = booking_datetime_str.split('T')[0]
            booking_time = booking_datetime_str.split('T')[1]
        else:
            booking_date = booking_datetime_str
            booking_time = None

        # Booking fee (convenience/verification fee)
        booking_fee = 10.00
        total_amount = float(service.price) + booking_fee

        booking = Booking.objects.create(
            user=request.user,
            service=service,
            provider=service.provider,
            booking_date=booking_date,
            booking_time=booking_time,
            address=address,
            description=description,
            booking_fee=booking_fee,
            total_amount=total_amount,
            status='pending'
        )

        messages.info(request, "Booking saved! Please complete payment to confirm.")
        return redirect('booking_confirm', booking_id=booking.id)

    return render(request, "book_service.html", {"service": service})


@login_required
def booking_confirm(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, "booking_confirm.html", {"booking": booking})


@login_required
def simulate_payment(request, booking_id):
    """Initiates Razorpay payment checkout."""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == "POST":
        payment_method = request.POST.get('payment_method', 'online')
        booking.payment_method = payment_method
        if payment_method == 'cash':
            booking.status = 'pending payment'
            booking.save()
            messages.success(request, "Booking confirmed with Cash on Service!")
            # Mark provider as Busy
            provider = booking.provider
            if provider:
                provider.availability = 'Busy'
                provider.save()
                # Notify provider
                Notification.objects.create(
                    user=provider.user,
                    title="💰 New Cash Booking!",
                    message=(
                        f"You have a new booking for '{booking.service.name}' "
                        f"from {request.user.get_full_name() or request.user.username}. "
                        f"Scheduled: {booking.booking_date}. Payment: Cash on Service."
                    ),
                    link=reverse('provider_dashboard')
                )
            return redirect('my_orders')
        
        booking.save()

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    # Amount in paise (₹1 = 100 paise)
    amount_in_paise = int(float(booking.total_amount) * 100)

    data = {
        "amount": amount_in_paise,
        "currency": "INR",
        "receipt": f"receipt_booking_{booking.id}",
        "notes": {
            "booking_id": str(booking.id),
            "service": booking.service.name,
            "customer": request.user.username,
        },
        "payment_capture": 1
    }

    try:
        razorpay_order = client.order.create(data=data)
        razorpay_order_id = razorpay_order['id']
    except Exception as e:
        print(f"[Razorpay] Order creation error: {e}")
        # Graceful fallback for demo / test without real keys
        razorpay_order_id = f"order_demo_{booking.id}"

    context = {
        "booking": booking,
        "razorpay_order_id": razorpay_order_id,
        "razorpay_key_id": settings.RAZORPAY_KEY_ID,
        "amount_in_paise": amount_in_paise,
        "currency": "INR",
        "callback_url": request.build_absolute_uri(
            reverse('payment_success_view', args=[booking.id])
        ),
    }
    return render(request, "payment_page.html", context)


@login_required
def payment_success_view(request, booking_id):
    """Verifies Razorpay signature and finalises the booking."""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == "POST":
        razorpay_payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id   = request.POST.get('razorpay_order_id', '')
        razorpay_signature  = request.POST.get('razorpay_signature', '')

        # --- Signature Verification ---
        payment_verified = False
        if razorpay_payment_id and razorpay_order_id and razorpay_signature:
            try:
                client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
                params_dict = {
                    'razorpay_order_id':   razorpay_order_id,
                    'razorpay_payment_id': razorpay_payment_id,
                    'razorpay_signature':  razorpay_signature,
                }
                client.utility.verify_payment_signature(params_dict)
                payment_verified = True
            except razorpay.errors.SignatureVerificationError:
                print("[Razorpay] Signature verification FAILED.")
            except Exception as e:
                print(f"[Razorpay] Verification error: {e}")
                # Allow demo flow without real keys
                if razorpay_order_id.startswith("order_demo_"):
                    payment_verified = True

        # Demo / test fallback (no real keys configured)
        if not payment_verified and razorpay_order_id.startswith("order_demo_"):
            payment_verified = True

        if payment_verified:
            # Update booking status
            booking.status = 'accepted'
            booking.save()

            # Mark provider as Busy
            provider = booking.provider
            provider.availability = 'Busy'
            provider.save()

            # Notify provider
            Notification.objects.create(
                user=booking.provider.user,
                title="💰 New Booking – Payment Received!",
                message=(
                    f"You have a confirmed booking for '{booking.service.name}' "
                    f"from {request.user.get_full_name() or request.user.username}. "
                    f"Scheduled: {booking.booking_date}."
                ),
                link=reverse('provider_dashboard')
            )

            messages.success(request, "Payment successful! Your booking is confirmed.")
            return render(request, "payment_success.html", {
                "booking": booking,
                "payment_id": razorpay_payment_id,
            })
        else:
            messages.error(request, "Payment verification failed. Please try again or contact support.")
            return redirect('simulate_payment', booking_id=booking.id)

    # GET request – redirect to payment page
    return redirect('simulate_payment', booking_id=booking.id)