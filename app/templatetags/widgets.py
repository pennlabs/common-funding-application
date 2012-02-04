from django import template
from django.template import RequestContext
from django.template.loader import render_to_string

from templatetag_sugar.register import tag

register = template.Library()

@tag(register, [])
def fundingbar(context):
  return render_to_string('templatetags/fundingbar.html', context)