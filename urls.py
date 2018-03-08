from django.conf.urls import include, url
from django.contrib import admin

from registration.backends.model_activation.views import RegistrationView
from django.contrib.auth.views import PasswordChangeView, PasswordResetView
from app.forms import RegistrationForm, PasswordChangeForm, PasswordResetForm

admin.autodiscover()

admin.site.site_header = "CFA administration"

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/password/change/$', PasswordChangeView.as_view(form_class=PasswordChangeForm, success_url="done"), name='auth_password_change'),
    url(r'^accounts/password/reset/$', PasswordResetView.as_view(form_class=PasswordResetForm, success_url="done"), name='auth_password_reset'),
    url(r'^accounts/register/$', RegistrationView.as_view(form_class=RegistrationForm), name='registration_register'),
    url(r'^accounts/', include('registration.backends.model_activation.urls')),
    url(r'', include('app.urls')),
]
