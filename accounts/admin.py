from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms.models import BaseInlineFormSet
from .models import CustomUser, UserProfile

# Custom Formset: Jo unique constraint error ko rokega
class UserProfileInlineFormSet(BaseInlineFormSet):
    def save_new(self, form, commit=True):
        # Agar signal ne pehle hi profile bana di hai, toh use fetch karein
        profile = self.instance.profile
        # Form se aane wale data se profile fields ko update karein
        for field, value in form.cleaned_data.items():
            if field not in ['id', 'user']:
                setattr(profile, field, value)
        if commit:
            profile.save()
        return profile

# User page ke andar hi Profile section dikhane ke liye StackedInline
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    formset = UserProfileInlineFormSet  # Custom formset link kiya
    can_delete = False
    verbose_name_plural = 'Profile'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'college_email', 'is_verified', 'is_staff', 'is_active')
    list_filter = ('is_verified', 'is_staff', 'is_active')
    
    # Custom fields (college_email aur is_verified) ko admin edit page par add karna
    fieldsets = UserAdmin.fieldsets + (
        ('College Details', {'fields': ('college_email', 'is_verified')}),
    )
    
    # User create karte time custom fields show karna
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('College Details', {'fields': ('college_email', 'is_verified')}),
    )

# Models ko register karna
admin.site.register(CustomUser, CustomUserAdmin)
