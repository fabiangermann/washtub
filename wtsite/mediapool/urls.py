from django.conf.urls.defaults import *

urlpatterns = patterns('wtsite.mediapool.views',     
    (r'^scan$', 'file_scanner'),
    #(r'^$', 'index'),
    )