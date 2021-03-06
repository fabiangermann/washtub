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

from django.conf.urls import patterns

urlpatterns = patterns('wtsite.mediapool.views',
    (r'^scan$', 'file_scanner'),
    (r'^scan/status$', 'scanner_status'),
    (r'^stream/(?P<hash_id>\S+)', 'stream'),
    (r'^stream_test$', 'stream_test_liq'),
    (r'^stream_test/(?P<hash_id>\S+)', 'stream_test'),
    #(r'^$', 'index'),
    )
