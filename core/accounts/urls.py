"""URL configuration for the accounts application."""

from django.urls import path

from . import views

urlpatterns = [
    # Home page
    path('', views.home_view, name='home'),

    # Authentication
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # User preferences
    path('set-timezone/', views.set_timezone, name='set_timezone'),
]