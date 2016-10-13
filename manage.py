#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    sys.path.append('/usr/lib/python2.7/site-packages/')
    sys.path.append('venv/lib/python2.7/site-packages/')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'wtsite.settings')

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
