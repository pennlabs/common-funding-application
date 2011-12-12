from django.forms import ModelForm
from django.shortcuts import render_to_response

from models import Application


def index(request):
  return render_to_response('index.html')

class ApplicationForm(ModelForm):
    class Meta:
        model = Application
