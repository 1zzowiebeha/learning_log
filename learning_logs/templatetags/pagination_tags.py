from typing import Type

from django import template

register = template.Library()

@register.filter(name='get_range') 
def get_range(number: str) -> range:
    return range(number)