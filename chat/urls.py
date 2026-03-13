from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_list, name='chat_list'),
    path('<int:user_id>/', views.chat_view, name='chat_view'),
    path('api/messages/<int:user_id>/', views.get_messages, name='get_messages'),
    path('api/unread-count/', views.unread_count, name='unread_count'),
]
