from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),
    path('tasks/create/', task_create, name='task_create'),
    path('tasks/edit/<int:task_id>/', task_edit, name='task_edit'),
    path('tasks/delete/<int:task_id>/', task_delete, name='task_delete'),
]
