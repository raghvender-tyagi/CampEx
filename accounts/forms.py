from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        # Kaun-kaun se fields sign up form par dikhane hain
        fields = ('username', 'college_email')

    def clean_college_email(self):
        email = self.cleaned_data.get('college_email')
        # Agar kisi ne email field empty chhoda hai toh validation error
        if not email:
            raise forms.ValidationError("College email is required.")
        return email

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'college_email', 'is_verified')


# Yeh code file ke bilkul end mein add kijiye:
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('branch', 'year', 'hostel', 'phone', 'profile_picture', 'bio')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }
