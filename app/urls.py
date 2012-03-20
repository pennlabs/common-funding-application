from django.conf.urls.defaults import patterns, include, url

import views


urlpatterns = patterns('',
    url(r'^$', views.shared.index),
    url(r'^apps$', apps_list),
    url(r'^form$', form),
    url(r'^itemlist$', itemlist),
    url(r'^itemlist-funder$', itemlist_funder),
    url(r'^delete_event', delete_event),
    url(r'^event', modify_event),
    url(r'^free-response$', free_response),
    url(r'^error', error),
    url(r'^funders/(\d+)/$', funders),
)
