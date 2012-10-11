from app.templatetags.helpers import funder_item_data, get_or_none
from app.models import *
from collections import namedtuple

from django import template
from django.template import RequestContext
from django.template.loader import render_to_string

from templatetag_sugar.parser import Variable, Optional, Constant, Name
from templatetag_sugar.register import tag


register = template.Library()
# question-answer pair
QA = namedtuple('QA', 'question answer')

@tag(register, [Variable(), Variable()])
def itemlist_requester(context, items, funded):
  """ Render the table of items in the requester view """
  # takes a dictionary of items
  new_context = {'items':items, 'funded':funded, 'CATEGORIES': CATEGORIES}
  return render_to_string('app/templatetags/itemlist-requester.html', new_context)



@tag(register, [Variable(), Variable(), Variable()])
def itemlist_funder(context, item_list, applied_funders, funder_id):
  """ Render the table of items in the funder view """
  items_data = []
  title_row = ['Name', 'Quantity', 'Price Per Unit', 'Total Amount', 'Category']
  for funder in applied_funders:
    title_row.append(funder.user.username)
  for item in item_list:
    items_data.append(funder_item_data(context, item, applied_funders))
  new_context = {
                  'titles': title_row,
                  'current_funder': funder_id,
                  'items_data': items_data
                }
  return render_to_string('app/templatetags/itemlist-funder.html', new_context)

@tag(register, [Variable(), Optional([Variable()])])
def application(context, user, event=None):
  if not event:
    event = None

  new_context = {
    'user'           : user,
    'event'          : event,
    'funder_qas'     : [QA(question, get_or_none(FreeResponseAnswer, question=question,event=event))
                        for question in FreeResponseQuestion.objects.all()],
    'eligibility_qas': [QA(question, get_or_none(EligibilityAnswer, question=question, event=event))
                        for question in EligibilityQuestion.objects.all()],
    'commonfreeresponse_qas': [QA(question, get_or_none(CommonFreeResponseAnswer, question=question, event=event))
                               for question in CommonFreeResponseQuestion.objects.all()],
    'funders'        : CFAUser.objects.filter(user_type='F')
  }

  if event.over:
    new_context['commonfollowup_qas'] = [QA(question, get_or_none(CommonFollowupAnswer, question=question, event=event))
                                         for question in CommonFollowupQuestion.objects.all()]
    new_context['followup_qas']       = [QA(question, get_or_none(FollowupAnswer, question=question, event=event))
                                         for question in FollowupQuestion.objects.all()]

  if not user.is_authenticated() or user.get_profile().is_funder \
    or event and event.funded:
    new_context['extra_attrs'] = 'disabled'
  return render_to_string('app/templatetags/application.html', new_context)
