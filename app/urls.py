from django.conf.urls import url

import views

urlpatterns = [
    url(r'^$', views.events, name='events'),
    url(r'^old/$', views.events_old, name='old-events'),
    url(r'^new/$', views.event_new, name='new-event'),
    url(r'^(\d+)/$', views.event_show, name='event-show'),
    url(r'^(\d+)/edit/$', views.event_edit, name='event-edit'),
    url(r'^(\d+)/destroy/$', views.event_destroy, name='event-destroy'),
    url(r'^funders/(\d+)/edit/$', views.funder_edit, name='funder-edit'),
]
