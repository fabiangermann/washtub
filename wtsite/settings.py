# Django settings for wtsite project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Specify the server name
# *Required trailing slash
SERVER_NAME = 'http://home.vinylproject.com/'

# djangologging options
INTERNAL_IPS = ('127.0.0.1',)
LOGGING_INTERCEPT_REDIRECTS = True

# Path configs for making Washtub Portable
# *Must have a starting slash
# *No trailing slash
PROJECT_PATH = '/usr/share/washtub'

# *No starting slash
# *Required trailing slash
BASE_URL = 'washtub/'

# These Are Custom Settings for the MediaPool App
MEDIAPOOL_PATH = '/mnt/nfs/lx-gateway/data/audio/washtub'

ADMINS = (
    ('Chris Everest', 'chris@vinylproject.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'washtubdb'             # Or path to database file if using sqlite3.
DATABASE_USER = 'cex'             # Not used with sqlite3.
DATABASE_PASSWORD = '6677rif'         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = PROJECT_PATH+'/www-static/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = SERVER_NAME+BASE_URL+'media/'

# Provide the URL for access denied redirects.
LOGIN_URL = '/'+BASE_URL+'login'
LOGIN_REDIRECT_URL = '/'+BASE_URL

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
# This URL path must point/link to the contrib admin media directory provided by Django
# i.e. ln -s /<your_project_path>/admin-media/ /<your_python_path>/django/contrib/admin/media
ADMIN_MEDIA_PREFIX = '/'+BASE_URL+'admin-media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '&)*b)wj5u$y+&qjo!@-4e*r!&zuixt*%g8%b1xm#jtcs$r*($-'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'wtsite.djangologging.middleware.LoggingMiddleware',
)

ROOT_URLCONF = 'wtsite.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_PATH+'/wtsite/templates', #this custom path must come first, to override the next
    '/usr/share/python-support/python-django/django/contrib/admin/templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'wtsite.controller',
    'wtsite.mediapool'
)

