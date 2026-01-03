"""URL configuration for the todo application."""

from django.urls import path

from . import views

urlpatterns = [
    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Task CRUD
    path('tasks/<int:task_id>/', views.task_view, name='task_view'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/edit/<int:task_id>/', views.task_edit, name='task_edit'),
    path('tasks/delete/<int:task_id>/', views.task_delete, name='task_delete'),
    path('tasks/toggle-completed/<int:task_id>/', views.toggle_completed, name='toggle_completed'),

    # Calendar
    path('calendar/', views.calendar_view, name='calendar_view'),

    # Categories
    path('categories/add/', views.add_category, name='add_category'),
]