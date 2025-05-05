from django import template
from persianfonts.cache import get_cached_active_font, set_cached_active_font
from persianfonts.models import Font

register = template.Library()

@register.simple_tag(name="get_persian_font",takes_context=True)
def get_persian_font(context):
    font = get_cached_active_font()
    if not font:
        font = Font.get_active_font()
        set_cached_active_font(font)
    return font


