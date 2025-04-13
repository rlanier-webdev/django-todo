from django.urls import path
from . import views

urlpatterns = [
    path('set-timezone/', views.set_timezone, name='set-timezone'),

    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('', views.home_view, name='home'),
]
