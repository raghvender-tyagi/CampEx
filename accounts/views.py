from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            # Success alert message
            messages.success(request, f'Account created for {username}! You can now login.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

# File ke top par ye import add kijiye:
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm

# Aur file ke end mein ye view function add kijiye:
@login_required
def profile(request):
    if request.method == 'POST':
        # instance=request.user.profile isliye kyunki hum naya record nahi bana rahe, existing update kar rahe hain
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        profile_form = UserProfileForm(instance=request.user.profile)
        
    return render(request, 'accounts/profile.html', {'profile_form': profile_form})

from django.contrib.auth import get_user_model
from listings.models import Listing

User = get_user_model()

def public_profile(request, username):
    other_user = get_object_or_404(User, username=username)
    active_listings = other_user.listings.filter(status='available').order_by('-created_at')
    
    allowed_domains = ['@kiet.edu', '@mycollege.in']
    is_email_validated = any(other_user.college_email.endswith(domain) for domain in allowed_domains)
    show_verified = other_user.is_active and is_email_validated

    wishlisted_ids = set()
    if request.user.is_authenticated:
        wishlisted_ids = set(request.user.wishlist_items.values_list('listing_id', flat=True))

    context = {
        'other_user': other_user,
        'active_listings': active_listings,
        'active_listings_count': active_listings.count(),
        'show_verified': show_verified,
        'wishlisted_ids': wishlisted_ids,
    }
    return render(request, 'accounts/public_profile.html', context)
