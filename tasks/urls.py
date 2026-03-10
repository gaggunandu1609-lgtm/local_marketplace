from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.post_task, name='post_task'),
    path('list/', views.task_list, name='task_list'),
    path('my-tasks/', views.my_tasks, name='my_tasks'),
    path('<int:task_id>/', views.task_detail, name='task_detail'),
]
