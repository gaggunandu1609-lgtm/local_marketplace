from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Notification
from django.contrib.auth.decorators import login_required

@login_required
def get_notifications(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
    # Store list of notifications to mark as read later
    notifications_list = list(notifications)
    # Mark them as read immediately so they don't appear in the next poll
    notifications.update(is_read=True)
    return render(request, "notifications/notification_toasts.html", {"notifications": notifications_list})

@login_required
def mark_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return JsonResponse({"status": "success"})
