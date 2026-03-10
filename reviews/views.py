from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from bookings.models import Booking
from .models import Review

@login_required
def submit_review(request, booking_id):
    # Use 'user' instead of 'customer'
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    # Use lowercase 'completed'
    if booking.status != 'completed':
        messages.error(request, "You can only review completed bookings.")
        return redirect('my_orders')

    if request.method == "POST":
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        # update_or_create to ensure one review per booking
        Review.objects.update_or_create(
            booking=booking,
            defaults={
                'user': request.user,
                'service': booking.service,
                'rating': rating,
                'comment': comment
            }
        )
        messages.success(request, "Review submitted successfully!")
        
        if request.headers.get('HX-Request'):
            # If HTMX, we could return a small success message or redirect header
            from django.http import HttpResponse
            response = HttpResponse("Review submitted successfully!")
            response['HX-Redirect'] = reverse('my_orders')
            return response
            
        return redirect('my_orders')
    
    return render(request, "review_form.html", {"booking": booking})
