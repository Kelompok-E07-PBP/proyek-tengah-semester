from django import template

register = template.Library()

@register.filter
def intdot(value):
    return f"{value:,.0f}".replace(",", ".")