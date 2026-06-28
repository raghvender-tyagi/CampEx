from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from .models import Notification
from messaging.models import Message

@login_required
def notification_list_view(request):
    notifications = Notification.objects.filter(recipient=request.user)
    
    # Mark all unread notifications as read on visit
    notifications.filter(is_read=False).update(is_read=True)
    
    return render(request, 'notifications/list.html', {
        'notifications': notifications
    })

@login_required
def unread_counts_api(request):
    unread_notifications = Notification.objects.filter(recipient=request.user, is_read=False).count()
    
    unread_messages = Message.objects.filter(
        Q(conversation__buyer=request.user) | Q(conversation__seller=request.user),
        is_read=False
    ).exclude(sender=request.user).count()
    
    return JsonResponse({
        'unread_notification_count': unread_notifications,
        'unread_message_count': unread_messages
    })

