import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

PROJECT_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(PROJECT_ROOT)


application = get_wsgi_application()
application = DjangoWhiteNoise(application)
