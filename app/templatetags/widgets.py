from django import template
from django.template import RequestContext
from django.template.loader import render_to_string

from templatetag_sugar.parser import Variable, Optional, Constant, Name
from templatetag_sugar.register import tag

from collections import namedtuple

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
