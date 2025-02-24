import os

import django
from channels.routing import get_default_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "penncfa.settings.production")
django.setup()
application = get_default_application()
