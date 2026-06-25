from django.urls import path
from . import views

app_name = 'listings'

urlpatterns = [
    path('', views.listing_feed, name='feed'),
    path('listing/<int:pk>/', views.listing_detail, name='detail'),
    path('listing/create/', views.listing_create, name='create'),
    path('listing/<int:pk>/delete/', views.listing_delete, name='delete'),
    path('my-listings/', views.my_listings, name='my_listings'),
    path('listing/<int:pk>/status/<str:status>/', views.mark_status, name='mark_status'),
    path('listing/<int:pk>/wishlist/', views.toggle_wishlist, name='toggle_wishlist'),
    path('wishlist/', views.wishlist_page, name='wishlist'),
]
