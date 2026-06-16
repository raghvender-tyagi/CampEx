from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # 1. Custom register view
    path('register/', views.register, name='register'),
    
    # 2. Built-in LoginView (jo automatic login verification handle karta hai)
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    
    # 3. Built-in LogoutView
    path('profile/', views.profile, name='profile'),
    
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
