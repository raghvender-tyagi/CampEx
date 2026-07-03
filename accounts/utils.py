from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings

def send_verification_email(request, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    current_site = get_current_site(request)
    
    protocol = 'https' if request.is_secure() else 'http'
    verification_url = f"{protocol}://{current_site.domain}/accounts/verify-email/{uid}/{token}/"
    
    subject = "Verify your CampusEx Account"
    
    context = {
        'user': user,
        'verification_url': verification_url,
    }
    
    # Render HTML message
    message_html = render_to_string('accounts/emails/verify_email.html', context)
    message_plain = f"Hi {user.username},\n\nPlease verify your email for CampusEx by clicking on the link below:\n{verification_url}\n\nHappy trading!"
    
    # Use console backend or settings configured one
    send_mail(
        subject=subject,
        message=message_plain,
        from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@campusex.in'),
        recipient_list=[user.college_email],
        html_message=message_html,
        fail_silently=False,
    )
