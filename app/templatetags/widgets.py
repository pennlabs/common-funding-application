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


@tag(register, [Variable()])
def itemlist_requester(context, items):
  # takes a dictionary of items
  new_context = {'items':items}
  return render_to_string('app/templatetags/itemlist-requester.html', new_context)


def get_or_none(model, **kwargs):
  """Get an object, or None."""
  try:
      return model.objects.get(**kwargs)
  except model.DoesNotExist:
      return None

# question-answer pair
QA = namedtuple('QA', 'question answer')

@tag(register, [Variable()])
def application(context, event):
  # TODO: Figure out a better way to get the request then passing it explicitly to the context
  request = context['request']
  new_context = RequestContext(request, {
      'event': event,
      'eligibility_qas': [QA(question, get_or_none(EligibilityAnswer, question=question, event=event))
          for question in EligibilityQuestion.objects.all()],
      'commonfreeresponse_qas': [QA(question, get_or_none(CommonFreeResponseAnswer, question=question, event=event))
          for question in CommonFreeResponseQuestion.objects.all()],
      'funders': CFAUser.objects.filter(user_type='F')
      })
  return render_to_string('app/templatetags/application.html', new_context)
