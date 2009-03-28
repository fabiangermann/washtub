from django.conf.urls.defaults import *

urlpatterns = patterns('wtsite.controller.views',     
	#(r'^control/(?P<host_name>\S+)$', 'display_status'),     
	(r'^control/skip/(?P<host_name>\S+)/(?P<stream>\S+)$', 'stream_skip'),
	(r'^$', 'index'),
	)