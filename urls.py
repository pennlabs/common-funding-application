from django.conf.urls.defaults import include, patterns, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.urls')),
    url(r'^application/(\d+)/', 'app.views.submitted'),
    url(r'', include('app.urls')),
)
