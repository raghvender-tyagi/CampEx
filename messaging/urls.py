from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('messages/', views.inbox_view, name='inbox'),
    path('messages/<int:pk>/', views.conversation_view, name='conversation'),
    path('messages/<int:pk>/updates/', views.get_new_messages, name='get_new_messages'),
    path('messages/start/<int:listing_id>/', views.start_conversation_view, name='start_conversation'),
    path('messages/start/user/<int:user_id>/', views.start_user_conversation_view, name='start_user_conversation'),
]
