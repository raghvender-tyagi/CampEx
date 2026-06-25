from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notification_list_view(request):
    notifications = Notification.objects.filter(recipient=request.user)
    
    # Mark all unread notifications as read on visit
    notifications.filter(is_read=False).update(is_read=True)
    
    return render(request, 'notifications/list.html', {
        'notifications': notifications
    })
