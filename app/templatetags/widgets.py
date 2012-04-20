from app.templatetags.helpers import funder_item_data
from app.models import CFAUser
from collections import namedtuple

from django import template
from django.template import RequestContext
from django.template.loader import render_to_string

from templatetag_sugar.parser import Variable, Optional, Constant, Name
from templatetag_sugar.register import tag

from app.models import *


register = template.Library()

@tag(register, [Variable(), Variable()])
def fundingbar(context, totalAmount, fundDict):
  # takes a dictionary {funder:amount}  
  
  FundItem = namedtuple('FundItem', ['funder', 'amount', 'percent'])
  fundItems = []
  currentAmount = 0;
  for k in fundDict:
    fundItems.append(FundItem(k,
                              amount=fundDict[k],
                              percent=fundDict[k]*100/totalAmount))
    currentAmount += fundDict[k];
    
  new_context = {'fundItems': fundItems,
                 'currentAmount': currentAmount,
                 'totalAmount': totalAmount}
  
  return render_to_string('app/templatetags/fundingbar.html', new_context)


@tag(register, [Variable(), Variable()])
def itemlist_requester(context, items, funded):
  # takes a dictionary of items
  new_context = {'items':items, 'funded':funded}
  return render_to_string('app/templatetags/itemlist-requester.html', new_context)



@tag(register, [Variable(), Variable()])
def itemlist_funder(context, item_list, funder_id):
  funders = CFAUser.objects.filter(user_type='F')
  items_data = []
  title_row = ['Name', 'Quantity', 'Price Per Unit', 'Total Amount']
  for funder in funders:
    title_row.append(funder.user.username)
  for item in item_list:
    items_data.append(funder_item_data(context, item, funders))
  new_context = {'titles': title_row,
                'current_funder': funder_id,
                'items_data': items_data}
  return render_to_string('app/templatetags/itemlist-funder.html', new_context)

def get_or_none(model, **kwargs):
  """Get an object, or None."""
  try:
      return model.objects.get(**kwargs)
  except model.DoesNotExist:
      return None

# question-answer pair
QA = namedtuple('QA', 'question answer')


@tag(register, [Variable(), Optional([Variable()])])
def application(context, user, event=None):
  if not event:
    event = None
  funders = CFAUser.objects.filter(user_type='F')
  funder_qs = {}
  for f in funders:
    funder_qs[f.id] = f.freeresponsequestion_set.all()
  new_context = {
      'user':user,
      'event': event,
      'funder_qs': funder_qs,
      'eligibility_qas': [QA(question, get_or_none(EligibilityAnswer, question=question, event=event))
          for question in EligibilityQuestion.objects.all()],
      'commonfreeresponse_qas': [QA(question, get_or_none(CommonFreeResponseAnswer, question=question, event=event))
          for question in CommonFreeResponseQuestion.objects.all()],
      'funders': funders
  }
  if not user.is_authenticated() or user.get_profile().is_funder \
    or event and event.funded:
    new_context['extra_attrs'] = 'disabled'
  return render_to_string('app/templatetags/application.html', new_context)
