from django.template.defaultfilters import stringfilter
from django.conf import settings
from django import template
import string

register = template.Library()

@register.filter("replacedot")
@stringfilter
def replacedot(value):
	return value.replace('(dot)', '.')

@register.filter("cat")
@stringfilter
def cat(value, string):
	return value+string

@register.filter("baseurl")
@stringfilter
def baseurl(value):
	return '/'+settings.BASE_URL+value


@register.filter("tominutes")
def tominutes(value):
	try:
		value = float(value)
		minutes = int(value/60)
		seconds = int(value%60)
		return ('%s:%.2d' % (minutes,seconds))
	except (ValueError, TypeError):
		return

