from django import forms
from django.http import HttpRequest

from .models import Topic, Entry, TopicHourData


class TopicForm(forms.ModelForm):
    """Topic modelform."""
    class Meta:
        model = Topic
        fields = ["content"]
        labels = {'content': 'Name'}
        widgets = {
            "content": forms.TextInput(),
        }


class EntryForm(forms.ModelForm):
    """Entry modelform."""
    class Meta:
        model = Entry
        fields = ["content"]
        labels = {'content': 'Entry:'}
        # verbose_name used as label
        
        widgets = {
            # long textarea
            "content": forms.Textarea(
                attrs={
                    'cols': 80,
                    'placeholder': 'Something new I learned...',
                }
            )
        }
        

class TopicHoursDataForm(forms.ModelForm):
    """A form to add or subtract hours spent learning a Topic.
    This isn't a ModelForm, since we aren't setting the number of hours.
    Rather, we add and subtract hours in the view."""
    
    class Meta:
        model = TopicHourData
        fields = ["hours", "created_on"]