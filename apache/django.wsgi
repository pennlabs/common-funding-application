import os, sys

import django.core.handlers.wsgi


PROJECT_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(PROJECT_ROOT)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

application = django.core.handlers.wsgi.WSGIHandler()
