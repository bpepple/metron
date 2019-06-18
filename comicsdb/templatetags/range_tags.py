from django import template

register = template.Library()


@register.filter
def cover_year_range(start, end):
    # Add 1 to end range to include current year
    x = sorted(range(start, int(end) + 1), reverse=True)
    return x
