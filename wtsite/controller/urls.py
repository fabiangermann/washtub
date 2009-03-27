from django.conf.urls.defaults import *

urlpatterns = patterns('wtsite.controller.views',     
	(r'^control/(?P<host_name>\S+)$', 'display_status'),     
	(r'^control/(?P<host_name>\S+)/(?P<rid>\d+)$', 'display_rid'),
	(r'^$', 'index'),
	)