from django.contrib import admin
from .models import Category, Listing, ListingImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    prepopulated_fields = {'slug': ('name',)}

class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'category', 'price', 'listing_type', 'condition', 'status', 'created_at')
    list_filter = ('listing_type', 'condition', 'status', 'category', 'created_at')
    search_fields = ('title', 'description', 'hostel_location')
    prepopulated_fields = {}
    inlines = [ListingImageInline]

admin.site.register(ListingImage)
