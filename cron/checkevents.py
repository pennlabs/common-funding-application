#!/usr/bin/env python
"""Checks whether an event is over and sends emails the requester if so"""

import os
import sys
from datetime import date, timedelta

from app.models import Event


PROJECT_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(PROJECT_ROOT)

os.environ["DJANGO_SETTINGS_MODULE"] = "settings"

DAYS = 3  # number of days to wait until sending an email
now = date.today()
events = Event.objects.all()

for event in events:
    if not event.followup_needed and not event.over:
        then = event.date
        if (now - then) > timedelta(days=DAYS):
            event.status = "W"
            event.save()
            event.notify_requester_for_followups()
            print(f"{event.name} has been over for more than {DAYS} days")
