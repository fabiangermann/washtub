from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.auth.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

admin.autodiscover()
urlpatterns = patterns('',
    # Example:
    # (r'^wtsite/', include('wtsite.foo.urls')),
    (r'^washtub/', include('wtsite.controller.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^washtub/admin/(.*)', admin.site.root),
    
    # Add Login URLS
    (r'^washtub/login/$', 'django.contrib.auth.views.login'),
    (r'^washtub/logout/$', 'django.contrib.auth.views.logout_then_login'),
    #Provide password reset 
    (r'^washtub/password_reset/$', 'django.contrib.auth.views.password_reset'),
    (r'^washtub/password_reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^washtub/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    (r'^washtub/reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
)
