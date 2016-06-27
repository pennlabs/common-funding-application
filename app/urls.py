from django.conf.urls import patterns, url

from views import *

urlpatterns = patterns('',
    url(r'^$',               events),
    url(r'^old/$',           events_old),
    url(r'^new/$',           event_new),
    url(r'^(\d+)/$',         event_show),
    url(r'^(\d+)/edit/$',    event_edit),
    url(r'^(\d+)/destroy/$', event_destroy),
    url(r'^funders/(\d+)/edit/$', funder_edit),
)
