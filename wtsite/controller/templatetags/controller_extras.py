from django.template.defaultfilters import stringfilter
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

@register.filter("tominutes")
def tominutes(value):
	try(float(value)):
		minutes = round(value/60)
		seconds = value % 60
		return ('%s:%s' % (minutes,seconds))
	except:
		return value
