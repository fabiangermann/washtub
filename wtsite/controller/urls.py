from django.conf.urls.defaults import *

urlpatterns = patterns('wtsite.controller.views',    
	(r'^control/skip/(?P<host_name>\S+)/(?P<stream>\S+)$', 'stream_skip'),     
	(r'^control/start/(?P<host_name>\S+)/(?P<stream>\S+)$', 'stream_start'),      
	(r'^control/stop/(?P<host_name>\S+)/(?P<stream>\S+)$', 'stream_stop'),
	(r'^queue/push/(?P<host_name>\S+)$', 'queue_push'),
	(r'^status/nodes/(?P<host_name>\S+)$', 'display_nodes'),
	(r'^status/queues/(?P<host_name>\S+)$', 'display_queues'),
	(r'^status/history/(?P<host_name>\S+)$', 'display_history'),
	(r'^status/help/(?P<host_name>\S+)$', 'display_help'),
	#(r'^status/search/(?P<host_name>\S+)/(?P<page>\d+)$', 'display_status_search_paged'),
	(r'^status/(?P<host_name>\S+)$', 'display_status'),
	(r'^pool/search/(?P<host_name>\S+)/(?P<page>\d+)$', 'search_pool_page'),
	(r'^pool/search/(?P<host_name>\S+)$', 'search_pool'),
	(r'^pool/(?P<host_name>\S+)/(?P<type>\S+)/(?P<page>\d+)$', 'display_pool_page'),     
	(r'^pool/(?P<host_name>\S+)/(?P<type>\S+)$', 'display_pool'),
	(r'^$', 'index'),
	)