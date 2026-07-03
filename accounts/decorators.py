from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect

def verification_required(view_func):
    """
    Decorator for views that checks if the logged-in user is verified.
    Redirects unverified users to the verification pending page.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Let login_required handle this if it's chained, or redirect to login.
            return redirect('login')
        if not request.user.is_verified:
            messages.warning(request, "Please verify your college email to perform this action.")
            return redirect('verification_pending')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
