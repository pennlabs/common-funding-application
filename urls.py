from django.conf.urls import include, url
from django.contrib import admin

from registration.backends.model_activation.views import RegistrationView
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView
from app.forms import RegistrationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm

admin.autodiscover()

admin.site.site_header = "CFA administration"

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/password/change/$', PasswordChangeView.as_view(form_class=PasswordChangeForm, success_url="done"), name='auth_password_change'),
    url(r'^accounts/password/reset/$', PasswordResetView.as_view(form_class=PasswordResetForm, success_url="done"), name='auth_password_reset'),
    url(r'^accounts/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmView.as_view(form_class=SetPasswordForm),
        name='password_reset_confirm'),
    url(r'^accounts/password/reset/complete/$', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    url(r'^accounts/register/$', RegistrationView.as_view(form_class=RegistrationForm), name='registration_register'),
    url(r'^accounts/', include('registration.backends.model_activation.urls')),
    url(r'', include('app.urls')),
]
