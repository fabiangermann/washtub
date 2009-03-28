from django import template

register = template.Library()

@register.filter
def replacedot(value):
	return value.replace('(dot)', '.')
