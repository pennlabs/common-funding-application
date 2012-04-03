from app.models import Event, EligibilityQuestion, EligibilityAnswer, \
    FreeResponseQuestion, FreeResponseAnswer, Grant, CFAUser, \
    CommonFreeResponseQuestion, CommonFreeResponseAnswer

def save_event(request):
  event_id = request.POST.get('event_id', None)
  event = Event.objects.get(pk=event_id)
  save_items(event, request)
  save_questions(event, request)

def save_items(event, request):
  item_names = request.POST.getlist('item_name')
  item_quantity = request.POST.getlist('item_quantity')
  item_price_per_unit = request.POST.getlist('item_price_per_unit')
  item_funding_already_received = request.POST.getlist('item_funding_already_received')
  item_category = request.POST.getlist('category')
  event.item_set.all().delete()
  for name, quantity, price_per_unit,funding, cat in zip(item_names,item_quantity,item_price_per_unit,item_funding_already_received, item_category):
    event.item_set.create(name=name, quantity=quantity, price_per_unit=price_per_unit, funding_already_received=funding, category=cat)

def save_questions(event, request):
  return
