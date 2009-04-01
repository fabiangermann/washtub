from django.conf.urls.defaults import *

urlpatterns = patterns('wtsite.mediapool.views',     
    (r'^mediapool/scan$', 'file_scanner'),
    #(r'^$', 'index'),
    )