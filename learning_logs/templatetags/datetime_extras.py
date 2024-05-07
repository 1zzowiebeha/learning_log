from datetime import datetime, timezone

from django import template
from django.utils.timezone import is_aware
from django.utils.translation import gettext_lazy
from django.utils.timesince import timesince
# ^ it's possible that timesince isn't localized. if so,
# update the custom_timesince filter to use the humanize way instead.

register = template.Library()

now_string = gettext_lazy("just now")
ago_string = gettext_lazy("ago") # might need some extra context for translation


def get_timesince_string(value, arg):
    if arg:
        return f"{timesince(value, arg)} {ago_string}"
    return f"{timesince(value)} {ago_string}"
    

@register.filter(name="custom_timesince", is_safe=False)
def custom_timesince_filter(value, arg=None):
    """Format a datetime as the time since that datetime (i.e. "4 days, 6 hours").
    If the deltatime is 0, return 'just now'.
    
    A mishmash of django.contrib.humanize, django.utils.timesince,
    and django.template.defaultfilters."""

    if not value:
        return ""
    try:
        now = datetime.now(timezone.utc if is_aware(value) else None)
        if value < now:
            delta = now - value
            if delta.days != 0:
                return get_timesince_string(value, arg)
            
            # bug: after 0 seconds, it becomes "0 minutes ago".
            # add all the logic from humanize here

            elif delta.seconds == 0:
                return now_string

        # else if value >= now, or value is within today,
        # but seconds != 0
        return get_timesince_string(value, arg)

    except (ValueError, TypeError):
        return ""