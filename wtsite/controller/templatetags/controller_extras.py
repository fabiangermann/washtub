#    Copyright (c) 2009, Chris Everest 
#    This file is part of Washtub.
#
#    Washtub is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Washtub is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Washtub.  If not, see <http://www.gnu.org/licenses/>.

from django.template.defaultfilters import stringfilter
from django.conf import settings
from django.utils.encoding import smart_str
from django import template
import string
import re

register = template.Library()

# Custom Filters Here
@register.filter("replacedot")
@stringfilter
def replacedot(value):
	return value.replace('(dot)', '.')

@register.filter("cat")
@stringfilter
def cat(value, string):
  return value+smart_str(string)

@register.filter("baseurl")
@stringfilter
def baseurl(value):
	return '/'+settings.BASE_URL+value

@register.filter("serverurl")
@stringfilter
def serverurl(value):
	return settings.SERVER_NAME+value

@register.filter("tominutes")
def tominutes(value):
	try:
		value = float(value)
		minutes = int(value/60)
		seconds = int(value%60)
		return ('%s:%.2d' % (minutes,seconds))
	except (ValueError, TypeError):
		return

@register.filter("basepath")
def basepath(value):
        return re.sub('^(.+\/)+', '', value);

@register.filter('subtract')
def subtract(value, operand):
  return value - operand

# Custom Template Here

@register.filter("truncatemiddle")
def do_truncatemiddle(value, new_size):
    size = len(smart_str(value))
    trunc = size - int(new_size) + 4 # Account for the size of the {..} ellipses we'll be adding
    if size - trunc <= 0 or new_size >= size: 
	# Account for the size of the ellipses
	return value
    f = int(round(new_size/3, 0))
    t = trunc
    regex = re.compile('^(.{%d,%d})(.{%d,%d})(.+)' % (f, f, t, t))
    new_list = regex.split(smart_str(value))
    if len(new_list) != 5:
        # Something didn't match correctly
        return value
    new_list[2] = '{..}'
    return ''.join(new_list)

@register.tag(name="queue_offset")
def do_queue_offset(parser, token):
    try:
        # XXX: This can only take a variable from context. 
        # Not sure how to pick or choose what's passed.
        tag_name, offset_value = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]
    return QueueOffsetNode(offset_value)

class QueueOffsetNode(template.Node):
    def __init__(self, offset_value):
        self.offset_value = template.Variable(offset_value)
    def render(self, context):
        try:
            offset = self.offset_value.resolve(context)
            context['queue_offset'] = offset
        except template.VariableDoesNotExist:
            return ''
        return ''
