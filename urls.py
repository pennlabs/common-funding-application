from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()

admin.site.site_header = "CFA administration"

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('registration.backends.model_activation.urls')),
    url(r'', include('app.urls')),
]
