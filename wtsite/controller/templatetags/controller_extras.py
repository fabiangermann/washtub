from django.template.defaultfilters import stringfilter
from django import template

register = template.Library()

@template.stringfilter
def replacedot(value):
	return value.replace('(dot)', '.')
