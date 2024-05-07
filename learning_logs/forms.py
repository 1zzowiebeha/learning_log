from django import forms
from django.http import HttpRequest
from django.core.exceptions import BadRequest
from stats.helperutils import max_length, get_total_hours

from .models import Topic, Entry, TopicHourData

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["content"]
        labels = {'content': 'Name'} # no label for content field
        widgets = {
            "content": forms.TextInput(),
        }


class EntryForm(forms.ModelForm):
    # Don't allow user to edit topic.
    # Set this in the view.
    class Meta:
        model = Entry
        fields = ["content"]
        labels = {'content': 'Entry:'}
        # verbose_name used as label
        widgets = {
            # long textarea
            "content": forms.Textarea(attrs=
                                      {'cols': 80,
                                       'placeholder': 'Something new I learned...'
                                      })
        }
        

class TopicHoursDataForm(forms.ModelForm):
    """A form to add or subtract hours spent learning a Topic.
    This isn't a ModelForm, since we aren't directly specifying
    the number of hours."""
    
    def __init__(self, request: HttpRequest, *args, **kwargs):
        if not request:
            raise ValueError("request must not be None")
        
        self.request = request
        super().__init__(*args, **kwargs)
    
    class Meta:
        model = TopicHourData
        fields = ["hours", "created_on"]
    
    # No, this shouldn't be in the form.
    # Views & forms are decoupled.
    # I think my code was wrong when I sent it,
    # .. hence why the guy was confused.
    # The view is the best place for this.
    # def clean_hours(self):
    #     # POSSIBLE RACE CONDITION
    #     data = self.cleaned_data["hours"]
    #     total_hours = get_total_hours(self.instance.topic)
        
    #     if "add" in self.request.POST:
    #         clamped_hours = max(0, min(total_hours + data, max_length))
    #         return clamped_hours
    #     elif "subtract" in self.request.POST:
    #         clamped_hours = max(0, min(total_hours - data, max_length))
    #         return clamped_hours
    #     else:
    #         raise BadRequest