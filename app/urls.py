from django.conf.urls.defaults import patterns, include, url

from views import *

urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^questionnaire', questionnaire),
    url(r'^apps$', apps_list),
    url(r'^form$', form),
    url(r'^itemlist$', itemlist),
    url(r'^itemlist-funder$', itemlist_funder),
    url(r'^login$', login),
    url(r'^logout$', logout),
    url(r'^delete_event', delete_event),
    url(r'^event', modify_event),
    url(r'^error', error),
)

