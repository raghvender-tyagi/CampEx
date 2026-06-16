from django.db import models
from django.conf import settings # accounts.CustomUser model ko safely reference karne ke liye

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Bootstrap icon class like 'bi-laptop'")
 
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
 
class Listing(models.Model):
    CONDITION_CHOICES = [
        ('new', 'New'), 
        ('like_new', 'Like New'), 
        ('good', 'Good'), 
        ('fair', 'Fair')
    ]
    STATUS_CHOICES = [
        ('available', 'Available'), 
        ('sold', 'Sold'), 
        ('rented', 'Rented')
    ]
    TYPE_CHOICES = [
        ('sell', 'Sell'), 
        ('rent', 'Rent'), 
        ('exchange', 'Exchange'), 
        ('free', 'Free')
    ]
 
    # settings.AUTH_USER_MODEL hume humare CustomUser model tak connect karega
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='listings')
    listing_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='sell')
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    hostel_location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views_count = models.PositiveIntegerField(default=0)
 
    def __str__(self):
        return self.title
 
class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='listings/%Y/%m/')
    is_primary = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"Image for {self.listing.title}"
