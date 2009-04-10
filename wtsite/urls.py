from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.auth.views import *
from django.conf import settings


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

admin.autodiscover()
urlpatterns = patterns('',
    # Example:
    # (r'^wtsite/', include('wtsite.foo.urls')),
    (r'^%s/', settings.BASE_URL, include('wtsite.controller.urls')),
    (r'^%s/mediapool/', settings.BASE_URL, include('wtsite.mediapool.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^%s/admin/(.*)', admin.site.root),
    
    # Add Login URLS
    (r'^%s/login/$', settings.BASE_URL, 'django.contrib.auth.views.login'),
    (r'^%s/logout/$', settings.BASE_URL, 'django.contrib.auth.views.logout_then_login'),
    #Provide password reset 
    (r'^%s/password_reset/$', settings.BASE_URL, 'django.contrib.auth.views.password_reset'),
    (r'^%s/password_reset/done/$', settings.BASE_URL, 'django.contrib.auth.views.password_reset_done'),
    (r'^%s/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', settings.BASE_URL, 'django.contrib.auth.views.password_reset_confirm'),
    (r'^%s/reset/done/$', settings.BASE_URL, 'django.contrib.auth.views.password_reset_complete'),
)
