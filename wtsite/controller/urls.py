from django.conf.urls.defaults import *

urlpatterns = patterns('wtsite.controller.views',    
	(r'^control/skip/(?P<host_name>\S+)/(?P<stream>\S+)$', 'stream_skip'),     
	(r'^control/start/(?P<host_name>\S+)/(?P<stream>\S+)$', 'stream_start'),      
	(r'^control/stop/(?P<host_name>\S+)/(?P<stream>\S+)$', 'stream_stop'), 
	(r'^status/(?P<host_name>\S+)$', 'display_status'),
	
	# group of media pool pages	     
	(r'^pool/(?P<host_name>\S+)/(?P<type>\S+)/(?P<page>\d+)$', 'display_pool_page'),     
	(r'^pool/(?P<host_name>\S+)/(?P<type>\S+)$', 'display_pool'),
	(r'^queue/(?P<host_name>\S+)/(?P<queue_name>\d+)$', 'queue_push'),
	(r'^$', 'index'),
	)