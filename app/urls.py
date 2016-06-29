from django.conf.urls import patterns, url

import views

urlpatterns = patterns(
    '',
    url(r'^$', views.events),
    url(r'^old/$', views.events_old),
    url(r'^new/$', views.event_new),
    url(r'^(\d+)/$', views.event_show, name='event-show'),
    url(r'^(\d+)/edit/$', views.event_edit, name='event-edit'),
    url(r'^(\d+)/destroy/$', views.event_destroy, name='event-destroy'),
    url(r'^funders/(\d+)/edit/$', views.funder_edit, name='funder-edit'),
)
