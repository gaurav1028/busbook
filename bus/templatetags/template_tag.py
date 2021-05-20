from django import template
import datetime

register = template.Library()

@register.filter
def subtract_days(value, days):
    return value - datetime.timedelta(days=days)