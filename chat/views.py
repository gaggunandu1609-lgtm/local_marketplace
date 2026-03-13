from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Message

@login_required
def chat_list(request):
    # Get all users the current user has chatted with
    sent_to = Message.objects.filter(sender=request.user).values_list('receiver', flat=True)
    received_from = Message.objects.filter(receiver=request.user).values_list('sender', flat=True)
    
    unique_user_ids = set(list(sent_to) + list(received_from))
    chat_users = User.objects.filter(id__in=unique_user_ids)
    
    return render(request, "chat/chat_list.html", {"chat_users": chat_users})

@login_required
def chat_view(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    
    if request.method == "POST":
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                content=content
            )
            
            # Simple AI simulation / auto-reply
            if hasattr(other_user, 'provider_profile') and not other_user.is_staff:
                import random
                replies = [
                    "Hello! Thanks for reaching out. I've received your message and will get back to you shortly.",
                    "Hi there! I'm currently on a job, but I'll check my schedule and reply within the hour.",
                    "Greetings! Thank you for inquiring about my services. How can I help you today?",
                    "Thanks for the message! I'm interested in your task. Let's discuss the details.",
                ]
                Message.objects.create(
                    sender=other_user,
                    receiver=request.user,
                    content=random.choice(replies)
                )

        if request.htmx:
            messages = Message.objects.filter(
                (Q(sender=request.user) & Q(receiver=other_user)) |
                (Q(sender=other_user) & Q(receiver=request.user))
            ).order_by('created_at')
            return render(request, "chat/_message_list.html", {"chat_messages": messages, "other_user": other_user})
        return redirect('chat_view', user_id=user_id)

    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=other_user)) |
        (Q(sender=other_user) & Q(receiver=request.user))
    ).order_by('created_at')
    
    # Mark as read
    Message.objects.filter(sender=other_user, receiver=request.user, is_read=False).update(is_read=True)

    context = {
        "other_user": other_user,
        "chat_messages": messages
    }
    
    return render(request, "chat/chat_detail.html", context)

@login_required
def get_messages(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=other_user)) |
        (Q(sender=other_user) & Q(receiver=request.user))
    ).order_by('created_at')
    
    return render(request, "chat/_message_list.html", {"chat_messages": messages, "other_user": other_user})

@login_required
def unread_count(request):
    count = Message.objects.filter(receiver=request.user, is_read=False).count()
    return render(request, "chat/_unread_count.html", {"count": count})
