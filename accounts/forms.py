from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

BRANCH_CHOICES = [
    ('', 'Select Branch'),
    ('CSE', 'Computer Science & Engineering'),
    ('IT', 'Information Technology'),
    ('ECE', 'Electronics & Communication'),
    ('EN', 'Electrical & Electronics'),
    ('ME', 'Mechanical Engineering'),
    ('CE', 'Civil Engineering'),
    ('Others', 'Others'),
]

YEAR_CHOICES = [
    (1, '1st Year'),
    (2, '2nd Year'),
    (3, '3rd Year'),
    (4, '4th Year'),
]

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True, label="Full Name")
    branch = forms.ChoiceField(choices=BRANCH_CHOICES, required=True)
    year = forms.ChoiceField(choices=YEAR_CHOICES, required=True)
    terms_accepted = forms.BooleanField(required=True, label="I agree to the Community Guidelines")

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'college_email')

    def clean_college_email(self):
        email = self.cleaned_data.get('college_email')
        if not email:
            raise forms.ValidationError("College email is required.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name')
        if commit:
            user.save()
            profile = user.profile
            profile.branch = self.cleaned_data.get('branch')
            profile.year = int(self.cleaned_data.get('year'))
            profile.save()
        return user

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

from django.contrib.auth.forms import AuthenticationForm

class EmailOrUsernameAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Username or Email"
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Enter your username or email'
        })

