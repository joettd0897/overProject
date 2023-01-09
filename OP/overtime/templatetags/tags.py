from django import template

register = template.Library()

@register.simple_tag
def minute_to_hour(value1):
    return value1 // 60

@register.simple_tag
def minute_to_minute(value1):
    return str(value1 % 60).zfill(2)