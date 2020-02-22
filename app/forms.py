from django import forms
from django.contrib.auth.forms import (PasswordChangeForm as BasePasswordChangeForm,
                                       PasswordResetForm as BasePasswordResetForm,
                                       SetPasswordForm as BaseSetPasswordForm)
from django.core.validators import RegexValidator
from django_registration.forms import RegistrationForm as BaseRegistrationForm

from .models import Event


class RegistrationForm(BaseRegistrationForm):
    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields["email"].label = "Penn Email Address"
        self.fields["email"].help_text = "Required. Email address ending with 'upenn.edu'"
        self.fields["email"].validators.append(RegexValidator(r"^.+@([a-zA-Z]*\.)?upenn\.edu$", "Enter a valid Penn email."))
        for f in self.fields.values():
            f.widget.attrs.update({"class": "form-control"})


class PasswordChangeForm(BasePasswordChangeForm):
    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs.update({"class": "form-control"})


class PasswordResetForm(BasePasswordResetForm):
    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.fields["email"].label = "Penn Email Address"
        self.fields["email"].validators.append(RegexValidator(r"^.+@([a-zA-Z]*\.)?upenn\.edu$", "Enter a valid Penn email."))
        for f in self.fields.values():
            f.widget.attrs.update({"class": "form-control"})


class SetPasswordForm(BaseSetPasswordForm):
    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs.update({"class": "form-control"})


class EventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super(EventForm, self).__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs.update({"class": "form-control"})
            if not f.required:
                f.help_text += " (optional)"

    def save(self, commit=True):
        m = super(EventForm, self).save(commit=False)

        if "submit-event" in self.data:
            m.status = "B"  # B for SUBMITTED
        else:
            m.status = "S"  # S for SAVED

        if self.instance.pk is not None:
            if m.followup_needed:
                m.status = "O"  # O for OVER
            elif m.funded:
                m.status = "F"  # F for FUNDED

        if commit:
            m.save()

        return m

    class Meta:
        model = Event
        fields = ["name", "date", "time", "location", "contact_name", "contact_email", "contact_phone", "anticipated_attendance",
                  "advisor_email", "advisor_phone", "organizations"]
        labels = {
            "name": "Event Name",
            "date": "Event Date",
            "time": "Event Time",
            "organizations": "Organization(s)",
        }
        help_texts = {
            "name": "Name of the event",
            "date": "Date of the event",
            "time": "Time of the event in 24-hour format",
            "location": "Location of the event",
            "contact_name": "Primary contact's name",
            "contact_email": "Primary contact's email address",
            "contact_phone": "Primary contact's phone number",
            "anticipated_attendance": "Anticipated number of people attending the event",
            "advisor_email": "Advisor's email address",
            "advisor_phone": "Advisor's phone number",
            "organizations": "Organization(s) involved with the event"
        }
