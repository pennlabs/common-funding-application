from django.conf.urls.defaults import patterns, include, url

import views


urlpatterns = patterns('',
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
)
