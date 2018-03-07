from django.conf.urls import include, url
from django.contrib import admin

from registration.backends.model_activation.views import RegistrationView
from app.forms import RegistrationForm

admin.autodiscover()

admin.site.site_header = "CFA administration"

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/register/$', RegistrationView.as_view(form_class=RegistrationForm), name='registration_register'),
    url(r'^accounts/', include('registration.backends.model_activation.urls')),
    url(r'', include('app.urls')),
]
