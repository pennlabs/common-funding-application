from django.contrib import admin
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from django.urls import include, re_path
from django_registration.backends.activation.views import RegistrationView

from app.forms import (
    PasswordChangeForm,
    PasswordResetForm,
    RegistrationForm,
    SetPasswordForm,
)


admin.autodiscover()

admin.site.site_header = "CFA administration"

urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
    re_path(
        r"^accounts/password/change/$",
        PasswordChangeView.as_view(form_class=PasswordChangeForm),
        name="auth_password_change",
    ),
    re_path(
        r"^accounts/password/reset/$",
        PasswordResetView.as_view(form_class=PasswordResetForm),
        name="auth_password_reset",
    ),
    re_path(
        r"^accounts/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        PasswordResetConfirmView.as_view(form_class=SetPasswordForm),
        name="password_reset_confirm",
    ),
    re_path(
        r"^accounts/password/reset/complete/$",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    re_path(
        r"^accounts/register/$",
        RegistrationView.as_view(form_class=RegistrationForm),
        name="registration_register",
    ),
    re_path(r"^accounts/", include("django_registration.backends.activation.urls")),
    re_path(r"^accounts/", include("django.contrib.auth.urls")),
    re_path(r"", include("app.urls")),
]
