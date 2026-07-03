from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

from .forms import EmailOrUsernameAuthenticationForm

urlpatterns = [
    # 1. Custom register view
    path('register/', views.register, name='register'),
    
    # 2. Built-in LoginView (jo automatic login verification handle karta hai)
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html',
        authentication_form=EmailOrUsernameAuthenticationForm
    ), name='login'),
    
    # 3. Built-in LogoutView
    path('profile/', views.profile, name='profile'),
    
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Email verification paths
    path('verify-email/<str:uidb64>/<str:token>/', views.verify_email, name='verify_email'),
    path('verification-pending/', views.verification_pending, name='verification_pending'),
    path('resend-verification/', views.resend_verification, name='resend_verification'),
]
