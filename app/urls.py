from django.urls import re_path

from . import views


urlpatterns = [
    re_path(r"^$", views.events, name="events"),
    # re_path(r'^old/$', views.events_old, name='old-events'),
    re_path(r"^new/$", views.event_new, name="new-event"),
    re_path(r"^(\d+)/$", views.event_show, name="event-show"),
    re_path(r"^(\d+)/edit/$", views.event_edit, name="event-edit"),
    re_path(r"^(\d+)/destroy/$", views.event_destroy, name="event-destroy"),
    # re_path(r'^(\d+)/download/$', views.event_download, name='event-download'),
    re_path(r"^funders/(\d+)/edit/$", views.funder_edit, name="funder-edit"),
    re_path(r"^export-requests/$", views.export_requests, name="export-requests"),
]
