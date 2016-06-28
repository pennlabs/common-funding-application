from django.conf.urls import patterns, url

from views import (events, events_old, event_new, event_show, event_edit,
                   event_destroy, funder_edit)

urlpatterns = patterns(
    '',
    url(r'^$', events),
    url(r'^old/$', events_old),
    url(r'^new/$', event_new),
    url(r'^(\d+)/$', event_show, name='event-show'),
    url(r'^(\d+)/edit/$', event_edit, name='event-edit'),
    url(r'^(\d+)/destroy/$', event_destroy, name='event-destroy'),
    url(r'^funders/(\d+)/edit/$', funder_edit, name='funder-edit'),
)
