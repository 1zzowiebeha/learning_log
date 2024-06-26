

from django import template

register = template.Library()

@register.filter(name='get_range') 
def get_range(value: int, start: int = 0, step: int = 1) -> range:
    """Return a range object for a
    template to iterate through."""
    # range is a C type, and cannot accept
    #   positional arguments
    return range(start,
                 value,
                 step)