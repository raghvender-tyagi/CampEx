from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver

# Placeholder validator to maintain backwards compatibility with old migrations
def validate_college_email(value):
    pass

# 2. Custom User Model
class CustomUser(AbstractUser):
    college_email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)

    @property
    def college_name(self):
        if self.college_email and '@' in self.college_email:
            domain = self.college_email.split('@')[1]
            parts = domain.split('.')
            if len(parts) > 1:
                # E.g. "kiet.edu" -> "KIET", "srm.ac.in" -> "SRM"
                domain_name = parts[0].upper()
                public_domains = ['GMAIL', 'YAHOO', 'OUTLOOK', 'HOTMAIL', 'ICLOUD', 'PROTON', 'PROTONMAIL', 'LIVE']
                if domain_name in public_domains:
                    return "STUDENT"
                return domain_name
            return domain.upper()
        return "STUDENT"

    def __str__(self):
        return self.username

# 3. User Profile Model
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    branch = models.CharField(max_length=100, blank=True)
    year = models.IntegerField(null=True, blank=True)
    hostel = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

# 4. Signals to auto-create and save UserProfile
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
