from django.conf.urls.defaults import patterns, include, url

from views import *


urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^form$', form),
    url(r'^itemlist-funder$', itemlist_funder),
    url(r'^free-response$', free_response),
    url(r'^events/$', events),
    url(r'^events/(\d+)/$', event_show),
    url(r'^events/(\d+)/answers/$', answers),
    url(r'^events/(\d+)/items/$', items),
    url(r'^events/(\d+)/funders/$', funders),
    url(r'^events/(\d+)/destroy/$', event_destroy),
    url(r'^error', error),
)
