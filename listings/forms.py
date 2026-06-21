from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'category', 'listing_type', 'condition', 'hostel_location']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe your item (e.g., brand, age, working condition, issues if any)...'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Enter price in INR (use 0 for free/exchange)'}),
            'hostel_location': forms.TextInput(attrs={'placeholder': 'e.g., VS Hostel, Room 302'}),
        }
