from django.conf.urls.defaults import patterns, include, url

from views import *

urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^event/(?P<event_id>\d+)/questionnaire$', questionnaire),
    url(r'^apps$', apps_list),
    url(r'^form$', form),
    url(r'^login$', login),
    url(r'^logout$', logout),
)

