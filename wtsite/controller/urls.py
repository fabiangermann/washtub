from django.conf.urls.defaults import *

urlpatterns = patterns('wtsite.controller.views',     
	(r'^control/skip/(?P<host_name>\S+)/(?P<stream>\S+)$', 'stream_skip'),     
	(r'^control/(?P<host_name>\S+)$', 'display_status'),
	(r'^$', 'index'),
	)