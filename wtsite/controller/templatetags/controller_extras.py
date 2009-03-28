from django.template.defaultfilters import stringfilter
from django import template

register = template.Library()

@register.filter(name='replacedot')
@template.stringfilter
def replacedot(value):
	return value.replace('(dot)', '.')
