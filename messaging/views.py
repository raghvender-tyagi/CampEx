from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import verification_required

from django.contrib import messages
from django.db.models import Q, Max
from django.db.models.functions import Coalesce
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib.auth import get_user_model
from .models import Conversation, Message
from listings.models import Listing
from notifications.models import Notification

User = get_user_model()

@login_required
def inbox_view(request):
    conversations = Conversation.objects.filter(
        Q(buyer=request.user) | Q(seller=request.user)
    ).annotate(
        last_message_time=Coalesce(Max('messages__created_at'), 'created_at')
    ).order_by('-last_message_time')

    for convo in conversations:
        convo.unread_count_val = convo.unread_count_for_user(request.user)

    return render(request, 'messaging/inbox.html', {
        'conversations': conversations
    })

@login_required
def conversation_view(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk)
    
    # Security check: only buyer or seller can view
    if request.user != conversation.buyer and request.user != conversation.seller:
        return HttpResponseForbidden("You are not authorized to view this conversation.")

    # Mark received messages as read
    conversation.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)

    if request.method == 'POST':
        body = request.POST.get('body', '').strip()
        if body:
            # Create message
            msg = Message.objects.create(
                conversation=conversation,
                sender=request.user,
                body=body
            )
            # Notify the other user
            recipient = conversation.get_other_user(request.user)
            listing_title = conversation.listing.title if conversation.listing else "profile"
            Notification.objects.create(
                recipient=recipient,
                notification_type='message',
                title=f"New message from {request.user.username} about {listing_title}",
                target_url=f"/messages/{conversation.pk}/"
            )
            
            # Check for AJAX request
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': {
                        'id': msg.id,
                        'body': msg.body,
                        'sender': msg.sender.username,
                        'created_at': msg.created_at.strftime('%d %b, %H:%M')
                    }
                })
                
            return redirect('messaging:conversation', pk=conversation.pk)

    # Get thread
    thread = conversation.messages.all()
    other_user = conversation.get_other_user(request.user)

    return render(request, 'messaging/conversation.html', {
        'conversation': conversation,
        'thread': thread,
        'other_user': other_user,
        'listing': conversation.listing
    })

@login_required
def get_new_messages(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk)
    
    # Security check: only buyer or seller can access
    if request.user != conversation.buyer and request.user != conversation.seller:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
        
    last_id = request.GET.get('last_id')
    if not last_id:
        return JsonResponse({'error': 'last_id parameter required'}, status=400)
        
    # Fetch messages newer than last_id
    new_messages = conversation.messages.filter(id__gt=last_id)
    
    # Mark received messages as read
    new_messages.exclude(sender=request.user).filter(is_read=False).update(is_read=True)
    
    messages_list = [{
        'id': msg.id,
        'body': msg.body,
        'sender': msg.sender.username,
        'created_at': msg.created_at.strftime('%d %b, %H:%M')
    } for msg in new_messages]
    
    return JsonResponse({'messages': messages_list})

@login_required
@verification_required
def start_conversation_view(request, listing_id):
    if request.method != 'POST':
        return HttpResponseForbidden("Method not allowed")
        
    listing = get_object_or_404(Listing, pk=listing_id)
    if listing.seller == request.user:
        messages.error(request, "You cannot start a conversation about your own listing.")
        return redirect('listings:detail', pk=listing_id)

    # get_or_create to find or create the conversation
    conversation, created = Conversation.objects.get_or_create(
        listing=listing,
        buyer=request.user,
        seller=listing.seller
    )
    return redirect('messaging:conversation', pk=conversation.pk)

@login_required
@verification_required
def start_user_conversation_view(request, user_id):
    other_user = get_object_or_404(User, pk=user_id)
    if other_user == request.user:
        messages.error(request, "You cannot message yourself.")
        return redirect('listings:feed')

    # Find or create conversation between this buyer and seller with listing=None
    conversation, created = Conversation.objects.get_or_create(
        listing=None,
        buyer=request.user,
        seller=other_user
    )
    return redirect('messaging:conversation', pk=conversation.pk)
