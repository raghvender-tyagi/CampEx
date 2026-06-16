from django.shortcuts import render, redirect
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
