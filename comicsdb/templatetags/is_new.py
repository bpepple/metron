from django import template
from django.utils import timezone

register = template.Library()


@register.filter
def is_new(added, days=1):
    days_new_deadline = timezone.now() - timezone.timedelta(days=days)
    return added > days_new_deadline
