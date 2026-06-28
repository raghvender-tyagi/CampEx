from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('notifications/', views.notification_list_view, name='list'),
    path('api/unread-counts/', views.unread_counts_api, name='unread_counts'),
]
