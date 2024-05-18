from django.forms import forms, ModelForm

from .models import UserProfile
    
class ProfileImageForm(ModelForm):
    """blah"""
    class Meta:
        model = UserProfile
        fields = ["profile_image"]