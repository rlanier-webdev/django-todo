from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),

    path('tasks/<int:task_id>/', task_view, name='task_view'),
    path('tasks/create/', task_create, name='task_create'),
    path('tasks/edit/<int:task_id>/', task_edit, name='task_edit'),
    path('tasks/delete/<int:task_id>/', task_delete, name='task_delete'),
    path('tasks/toggle-completed/<int:task_id>/', toggle_completed, name='toggle_completed'),

    path('calendar/', calendar_view, name='calendar_view'),

]
