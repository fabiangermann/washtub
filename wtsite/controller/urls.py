from django.conf.urls.defaults import *

urlpatterns = patterns('wtsite.controller.views',     
	(r'^status$', 'display_status'),
	)