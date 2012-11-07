from django.conf.urls.defaults import patterns, include, url

from views import *

urlpatterns = patterns('',
    url(r'^$',               events),
    url(r'^new/$',           event_new),
    url(r'^(\d+)/$',         event_show),
    url(r'^(\d+)/edit/$',    event_edit),
    url(r'^(\d+)/items/$',   items),
    url(r'^(\d+)/destroy/$', event_destroy),
)
