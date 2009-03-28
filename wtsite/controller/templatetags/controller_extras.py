from django.template.defaultfilters import stringfilter
from django import template
import string

register = template.Library()

@register.filter()
@stringfilter
def replacedot(value):
	return value.replace('(dot)', '.')
