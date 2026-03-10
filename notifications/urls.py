from django.urls import path
from . import views

urlpatterns = [
    path('get/', views.get_notifications, name='get_notifications'),
    path('mark-read/<int:notification_id>/', views.mark_read, name='mark_read'),
]
