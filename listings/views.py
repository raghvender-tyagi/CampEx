from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Category, Listing, ListingImage
from .forms import ListingForm

def listing_feed(request):
    if not request.user.is_authenticated:
        return render(request, 'listings/onboarding.html')
        
    listings = Listing.objects.filter(status='available').order_by('-created_at')
    categories = Category.objects.all()

    # Personalization: Near your hostel
    user_profile = getattr(request.user, 'profile', None)
    user_hostel = user_profile.hostel if user_profile else None
    near_listings = []
    if user_hostel:
        near_listings = listings.filter(hostel_location__icontains=user_hostel).exclude(seller=request.user)[:3]

    # Search filter
    query = request.GET.get('q')
    if query:
        listings = listings.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(hostel_location__icontains=query)
        )

    # Category filter
    category_slug = request.GET.get('category')
    if category_slug:
        listings = listings.filter(category__slug=category_slug)

    # Listing Type filter
    listing_type = request.GET.get('type')
    if listing_type:
        listings = listings.filter(listing_type=listing_type)

    wishlisted_ids = set()
    if request.user.is_authenticated:
        wishlisted_ids = set(request.user.wishlist_items.values_list('listing_id', flat=True))

    context = {
        'listings': listings,
        'near_listings': near_listings,
        'user_hostel': user_hostel,
        'categories': categories,
        'selected_category': category_slug,
        'selected_type': listing_type,
        'query': query,
        'wishlisted_ids': wishlisted_ids,
    }
    return render(request, 'listings/feed.html', context)

def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    
    # Increment views count
    listing.views_count += 1
    listing.save(update_fields=['views_count'])
    
    # Get primary image and other images
    primary_image = listing.images.filter(is_primary=True).first()
    if not primary_image:
        primary_image = listing.images.first()
    other_images = listing.images.all()

    context = {
        'listing': listing,
        'primary_image': primary_image,
        'other_images': other_images,
    }
    return render(request, 'listings/detail.html', context)

@login_required
def listing_create(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()

            # Handle multiple images
            images = request.FILES.getlist('images')
            for index, img in enumerate(images):
                is_primary = (index == 0) # Set first image as primary
                ListingImage.objects.create(
                    listing=listing,
                    image=img,
                    is_primary=is_primary,
                    order=index
                )
            
            messages.success(request, 'Your listing has been posted successfully!')
            return redirect('listings:feed')
    else:
        form = ListingForm()
    
    return render(request, 'listings/create.html', {'form': form})

@login_required
def listing_delete(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if listing.seller != request.user:
        messages.error(request, 'You do not have permission to delete this listing.')
        return redirect('listings:detail', pk=pk)
    
    listing.delete()
    messages.success(request, 'Your listing was successfully deleted!')
    return redirect('listings:feed')

@login_required
def my_listings(request):
    user_listings = Listing.objects.filter(seller=request.user).order_by('-created_at')
    
    # We can filter based on status tab:
    status_filter = request.GET.get('status', 'available')
    if status_filter in ['available', 'sold', 'rented']:
        filtered_listings = user_listings.filter(status=status_filter)
    else:
        filtered_listings = user_listings
        
    context = {
        'listings': filtered_listings,
        'selected_status': status_filter,
        'active_count': user_listings.filter(status='available').count(),
        'sold_count': user_listings.filter(status='sold').count(),
        'rented_count': user_listings.filter(status='rented').count(),
    }
    return render(request, 'listings/my_listings.html', context)

@login_required
def mark_status(request, pk, status):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)
    old_status = listing.status
    if status in ['available', 'sold', 'rented']:
        listing.status = status
        listing.save(update_fields=['status'])
        messages.success(request, f"Listing status updated to {status.capitalize()}.")
        
        # Trigger notifications if status changed to 'sold'
        if status == 'sold' and old_status != 'sold':
            from notifications.models import Notification
            wishlist_users = listing.wishlisted_by.values_list('user', flat=True)
            for user_id in wishlist_users:
                Notification.objects.create(
                    recipient_id=user_id,
                    notification_type='wishlist_sold',
                    title=f"{listing.title} has been sold",
                    target_url=f"/profile/{listing.seller.username}/"
                )
    return redirect('listings:my_listings')

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Wishlist

@login_required
@require_POST
def toggle_wishlist(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    wishlist_item = Wishlist.objects.filter(user=request.user, listing=listing)
    if wishlist_item.exists():
        wishlist_item.delete()
        wishlisted = False
    else:
        Wishlist.objects.create(user=request.user, listing=listing)
        wishlisted = True
    
    count = Wishlist.objects.filter(listing=listing).count()
    return JsonResponse({
        'wishlisted': wishlisted,
        'count': count
    })

@login_required
def wishlist_page(request):
    wishlists = Wishlist.objects.filter(user=request.user).select_related('listing').order_by('-saved_at')
    listings = [w.listing for w in wishlists]
    return render(request, 'listings/wishlist.html', {
        'listings': listings,
        'wishlist_count': len(listings)
    })
