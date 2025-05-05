from django import template
from notices.models import *
register = template.Library()

@register.simple_tag(name='get_news_count')
def get_news_count(id):
    count = News.objects.filter(newscat_id=id).count()
    return count