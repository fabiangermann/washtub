from django.conf.urls.defaults import *

urlpatterns = patterns('wtsite.controller.views',     
	(r'^control/status$', 'display_status'),
	(r'^$', 'index'),
	)