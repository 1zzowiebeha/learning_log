"""Define forms for the profiles app."""

from django import forms

from .models import UserProfile

        
class ProfileSettingsForm(forms.ModelForm):
    """A list of UserProfile fields
    for a user to edit."""
    class Meta:
        model = UserProfile
        fields = ["profile_image", "bio_text", "is_public"]
        
        widgets = {
            'bio_text': forms.TextInput(
                attrs={
                    'placeholder': 'A bit about me...',
                }
            ),
        }
        
        labels = {
            'is_public': 'Public to non-friends'
        }