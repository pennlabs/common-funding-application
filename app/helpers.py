from app.models import Event, EligibilityQuestion, EligibilityAnswer, \
    FreeResponseQuestion, FreeResponseAnswer, Grant, CFAUser, \
    CommonFreeResponseQuestion, CommonFreeResponseAnswer

def save_event(request):
  name = request.POST.get('name')
  date = request.POST.get('date')
  requester = request.user.cfauser
  location = request.POST.get('location')
  organizations = request.POST.get('organizations')
  event_id = request.POST.get('event_id', None)
  if event_id == "":
    event = Event.objects.create(
        name=name,
        date=date,
        requester=requester,
        location=location,
        organizations=organizations
        )
  else:
    event = Event.objects.get(pk=event_id)
    event.date = date
    event.name = name
    event.organizations = organizations
    event.location = location
    event.save()
  save_items(event, request)

  #event, _ = Event.objects.get_or_create(name=name, date=date, requester=requester,
  #    defaults={'location':location,'organizations':organizations})
  # save_all_questions(event, request)

def save_items(event, request):
  item_names = request.POST.getlist('item_name')
  item_quantity = request.POST.getlist('item_quantity')
  item_price_per_unit = request.POST.getlist('item_price_per_unit')
  item_funding_already_received = request.POST.getlist('item_funding_already_received')
  item_category = request.POST.getlist('item_category')
  event.item_set.all().delete()
  for name, quantity, price_per_unit,funding, cat in zip(item_names,item_quantity,item_price_per_unit,item_funding_already_received, item_category):
    event.item_set.create(name=name, quantity=quantity, price_per_unit=price_per_unit, funding_already_received=funding, category=cat)

def save_all_questions(event, request):
  eligibility_answers = request.POST.getlist('eligibility_answers')
  event.eligibilityanswer_set.all().delete()
  for answer in eligibility_answers:
    event.eligibilityanswer_set.create(question='gfdgdgd',event=event,answer=answer)
  
  commonresponse_answers = request.POST.getlist('commonresponse_answers')
  event.commonfreeresponseanswer_set.all().delete()
  for answer in commonresponse_answers:
    event.commonfreeresponseanswer_set.create(question='fgfdgfd',event=event,answer=answer)
  
  freeresponse_answers = request.POST.getlist('freeresponse_answers')
  event.freeresponseanswer_set.all().delete()
  for answer in freeresponsei_answers:
    event.freeresponseanswer_set.create(question='test',event=event,answer=answer)
