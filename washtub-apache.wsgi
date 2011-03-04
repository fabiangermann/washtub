import os
import sys

path = '/usr/share/washtub'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'wtsite.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
