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
from django import template
import hashlib

register = template.Library()

# Custom Filters Here
@register.filter("media_hash")
@stringfilter
def url_hash(value, hasher):
    # Create a new media hash
    t = hashlib.new('ripemd160')
    t.update("%s%s%s" % (value, hasher, settings.MEDIAPOOL_KEY))
    return t.hexdigest()
