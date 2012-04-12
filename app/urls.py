from django.conf.urls.defaults import patterns, include, url

from views import *


urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^events/$', events),
    url(r'^events/new/$', event_new),
    url(r'^events/(\d+)/$', event_show),
    url(r'^events/(\d+)/edit/$', event_edit),
    url(r'^events/(\d+)/items/$', items),
    url(r'^events/(\d+)/funders/$', funders),
    url(r'^events/(\d+)/funders/(\d+)/application/', free_response),
    url(r'^events/(\d+)/destroy/$', event_destroy),
    url(r'^application/', application),
)
