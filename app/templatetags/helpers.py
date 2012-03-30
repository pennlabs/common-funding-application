from django import template

from app.models import Grant

from templatetag_sugar.parser import Variable, Optional, Constant, Name
from templatetag_sugar.register import tag


register = template.Library()

@tag(register, [Variable(), Variable()])
def funders_grant_to_item(context, item, funder):
  grant = Grant.objects.filter(item=item, funder=funder.cfauser)
  return grant[0].amount if grant else 0
  
