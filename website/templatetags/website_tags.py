from django import template
from website.models import Config
register = template.Library()

@register.simple_tag(name='get_website_info')
def get_website_info(value):
    header = Config.objects.get(key=value)
    return header
