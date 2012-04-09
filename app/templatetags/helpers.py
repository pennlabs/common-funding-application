from django import template
from django.template.loader import render_to_string

from app.models import Grant, CFAUser

from templatetag_sugar.parser import Variable, Optional, Constant, Name
from templatetag_sugar.register import tag


register = template.Library()

def funders_grant_data_to_item(context, item, funder_id):
  grant = Grant.objects.filter(item=item, funder__id=funder_id)
  return (grant[0].amount, grant.id) if grant else (0, 0)
  
def funder_item_data(context, item, funders):
  item_data = [item.name, item.quantity, item.price_per_unit, item.total]
  funders_data = []
  for funder in funders:
    grant_amount, grant_id = funders_grant_data_to_item(context, item, funder.id)
    funders_data.append((funder.id, grant_amount, grant_id))
  return (item_data, funders_data)

@tag(register, [Variable(), Variable()])
def funder_item_table(context, item_list, funder_id):
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
  return render_to_string('app/templatetags/funder_item_table.html', new_context)
