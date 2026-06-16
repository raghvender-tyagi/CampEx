from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver

# 1. Custom validator for College Email
def validate_college_email(value):
    allowed_domains = ['@kiet.edu', '@mycollege.in']
    if not any(value.endswith(domain) for domain in allowed_domains):
        raise ValidationError(
            f"Only emails from these domains are allowed: {', '.join(allowed_domains)}"
        )

# 2. Custom User Model
class CustomUser(AbstractUser):
    college_email = models.EmailField(unique=True, validators=[validate_college_email])
    is_verified = models.BooleanField(default=False)

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
