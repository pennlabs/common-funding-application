from app.models import Grant


def funders_grant_data_to_item(context, item, funder_id):
  grant = Grant.objects.filter(item=item, funder__id=funder_id)
  return (grant[0].amount, item.id) if grant else (None, item.id)

def funder_item_data(context, item, funders):
  item_data = [item.name, item.quantity, '$'+str(item.price_per_unit), '$'+str(item.total), item.get_category_display()]
  funders_data = []
  for funder in funders:
    grant_amount, grant_id = funders_grant_data_to_item(context, item, funder.id)
    funders_data.append((funder.id, grant_amount, grant_id))
  return (item_data, funders_data)

def get_or_none(model, **kwargs):
  """Get an object, or None."""
  try:
    return model.objects.get(**kwargs)
  except model.DoesNotExist:
    return None
