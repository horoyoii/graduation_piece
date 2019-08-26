from django import template
from datetime import datetime

register = template.Library()



@register.simple_tag
def number_of_messages(request):
    return 123456

@register.simple_tag            # 2
def today():
    print("Called today")
    return datetime.now().strftime("%Y-%m-%d %H:%M")

