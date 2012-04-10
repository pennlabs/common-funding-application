import os
from collections import namedtuple

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string

from sandbox_config import URL_ROOT

from app.forms import EventForm, EligibilityQuestionnaireForm, BudgetForm, \
    FreeResponseForm
from app.models import Event, EligibilityQuestion, EligibilityAnswer, \
    FreeResponseQuestion, FreeResponseAnswer, Grant, CFAUser, \
    CommonFreeResponseQuestion, CommonFreeResponseAnswer


NOT_AUTHORIZED = 'app.views.index'

def index(request):
    return redirect('app.views.events')


def authorization_required(view):
  """Ensure only a permitted user can access an event.
  A user is permitted if:
    * They requested the event
    * They are a funder
    * They have a secret key to an event
  """
  def protected_view(request, event_id, *args, **kwargs):
    user = request.user.get_profile()
    event = Event.objects.get(pk=event_id)
    if user.is_funder or user.requested(event):
      return view(request, event_id, *args, **kwargs)
    else:
      try:
        key = request.GET['key']
      except KeyError:
        return redirect(NOT_AUTHORIZED)
      else:
        if key == event.secret_key:
          return view(request, event_id, *args, **kwargs)
        else:
          return redirect(NOT_AUTHORIZED)
  return protected_view


def requester_only(view):
  """Ensure only the user who requested the event can access a page."""
  def protected_view(request, event_id, *args, **kwargs):
    user = request.user
    event = Event.objects.get(pk=event_id)
    if user.get_profile().requested(event):
      return view(request, event_id, *args, **kwargs)
    else:
      return redirect(NOT_AUTHORIZED)
  return protected_view


@login_required
def events(request):
  if request.method == 'POST':
    # handle Create
    event = Event.objects.create(name=request.POST['name'],
                                 date=request.POST['date'],
                                 location=request.POST['location'],
                                 organizations=request.POST['organizations'],
                                 requester=request.user.cfauser)
    # handle questions
    for key, value in request.POST.items():
      if key.endswith("?"):
        question = EligibilityQuestion.objects.get(question=key)
        event.eligibilityanswer_set.create(question=question, answer=value)
    return redirect('app.views.items', event.id)
  elif request.method == 'GET':
    user = request.user
    if user.get_profile().is_requester:
      apps = Event.objects.filter(requester=user.get_profile()).extra(order_by=['date'])
    else: #TODO: filter for funders once submitting functionality has been implemented
      apps = user.get_profile().event_applied_funders.all().extra(order_by=['date'])
    # TEST DATA
    test_grant_total = 1200
    test_grants = {'SCUE' : 600,
                   'T-Change' : 300,
                   'Faith Fund' : 50}
      
    return render_to_response('app/events.html',
                              {'apps': apps,
                               'test_grant_total': test_grant_total,
                               'test_grants': test_grants},
                              context_instance=RequestContext(request))
  else:
    return HttpResponseNotAllowed(['GET', 'POST'])


@login_required
def event_new(request):
  """Form to create a new event."""
  if request.method == 'POST':
    save_event(request)
    return redirect('app.views.events')
  elif request.method == 'GET':
    return render_to_response('app/application.html',
        context_instance=RequestContext(request))
  else:
    return HttpResponseNotAllowed(['GET'])


@login_required
@requester_only
def event_edit(request, event_id):
  user = request.user
  if request.method == 'GET':
    event = Event.objects.get(pk=event_id)
    items = event.item_set.all()
    eligibility = event.eligibilityanswer_set.all()
    common = event.commonfreeresponseanswer_set.all()
    free = event.freeresponseanswer_set.all()
    organizations = event.organizations
    location = event.location

    # can't get the event's funders?
    return render_to_response('app/application.html',
        {
          'event': event,
          'items':items,
          'eligibility':eligibility,
          'commonresponse':common,
          'freeresponse':free,
          'organizations':organizations,
          'location':location,
          'funders': funders
        },
        context_instance=RequestContext(request))
  else:
    return HttpResponseNotAllowed(['GET'])


@login_required
@authorization_required
def event_show(request, event_id):
  user = request.user
  event = Event.objects.get(pk=event_id)
  if request.method == 'POST': #TODO: should really be PUT
    if user.cfauser.is_funder:
      for item in event.item_set.all():
        amount = request.POST.get("item_" + str(item.id), None)
        grants = []
        if amount:
          amount = int(amount)
          grant, _ = Grant.objects.get_or_create(funder=user.cfauser,
                                              item=item,
                                              defaults={'amount': 0})[0]
          amount_funded = sum(grant.amount for grant in 
              Grant.objects.filter(item=item))

          # if the funder gave too much, adjust the price to be only enough
          if amount + amount_funded - grant.amount > item.amount:
            amount = item.amount - amount_funded + grant.amount

          grant.amount = amount
          grant.save()

          grants.append(grant)

        if grants:
          # email the event requester indicating that they've been funded
          event.notify_requester(grants)
          funder.notify_osa(event, grants)
      return redirect('app.views.event_show', event_id)
    else:
      for key, value in request.POST.items():
        if key in ('csrfmiddlewaretoken', 'event_id'):
          continue
        if key == 'name':
          event.name = value
        elif key == 'date':
          event.date = value
        elif key == 'location':
          event.location = value
        elif key == 'organizations':
          event.organizations = value
        elif key.endswith("?"):
          question = EligibilityQuestion.objects.get(question=key)
          try:
            answer = event.eligibilityanswer_set.get(question=question)
          except EligibilityAnswer.DoesNotExist:
            event.eligibilityanswer_set.create(question=question,
                                    answer=value)
          else:
            answer.answer = value
            answer.save()
      event.save()
      return redirect('app.views.items', event_id)
  elif request.method == 'GET':
    event = Event.objects.get(pk=event_id)
    form = EventForm(event)
    if user.cfauser.is_funder:
      for key in form.fields:
        form.fields[key].widget.attrs['disabled'] = True
      other_form = FreeResponseForm(event_id, user.cfauser.id)
      for key in other_form.fields:
        other_form.fields[key].widget.attrs['disabled'] = True
    else:
      other_form = None
    return render_to_response('app/event-edit.html',
      {'form': form, 'event': event, 'is_funder':user.cfauser.is_funder,
      'other_form': other_form, 'funder_id':user.cfauser.id,
      'cfauser_id': user.cfauser.id},
      context_instance=RequestContext(request))
  else:
    return HttpResponseNotAllowed(['POST'])

@login_required
@requester_only
def items(request, event_id):
  user = request.user
  if request.method == 'POST':
    event_id = request.POST.get('event_id', None)
    event = Event.objects.get(pk=event_id)
    item_names = request.POST.getlist('item_name')
    item_amounts = request.POST.getlist('item_amount')
    item_units = request.POST.getlist('item_units')
    event.item_set.all().delete()
    for name, amount, units in zip(item_names, item_amounts, item_units):
      event.item_set.create(name=name, amount= amount, units=units, funding_already_received=0)
    return redirect('app.views.funders', event_id)
  elif request.method == 'GET':
    event = Event.objects.get(pk=event_id)
    return render_to_response('app/itemlist.html',
                              {'event': event},
                              context_instance=RequestContext(request))
  else:
    return HttpResponseNotAllowed(['GET', 'POST'])

def itemlist_funder(request, event_id):
  user = request.user
  if user.is_authenticated():
    if request.method == 'GET':
      try:
        event = Event.objects.get(pk=event_id)
        event_name = event.name
      except Event.DoesNotExist:
        return render_to_response('error.html',
                                  {'error_message': "Unable to view event"},
                                  context_instance=RequestContext(request))
      return render_to_response('itemlist-funder.html',
                                {'event': event},
                                context_instance=RequestContext(request))

    elif request.method == 'POST':
      event_id = request.POST.get('event_id', None)
      try:
        event = Event.objects.get(pk=event_id)
      except Event.DoesNotExist:
        return render_to_response('error.html',
                                  {'error_message': "Unable to modify event"},
                                  context_instance=RequestContext(request))
      for item in event.item_set.all():
        amount = request.POST.get("item_" + str(item.id), None)
        if amount and int(amount):
          amount = int(amount)
          grant = Grant.objects.get_or_create(funder=user.cfauser,
                                              item=item,
                                              defaults={'amount': 0})[0]
          grants = Grant.objects.filter(item=item)
          amount_funded = sum(grant.amount for grant in grants)
          if amount + amount_funded > item.amount:
            amount = item.amount - amount_funded
          grant.amount = grant.amount + amount
          grant.save()
      return render_to_response('itemlist-funder.html',
                                {'event': event},
                                context_instance=RequestContext(request))
  else:
    return HttpResponseNotAllowed(['GET', 'POST'])


@login_required
@requester_only
def event_destroy(request, event_id):
  event = Event.objects.get(pk=event_id)
  event.delete()
  return redirect('app.views.events')


@login_required
@requester_only
def free_response(request, event_id, funder_id):
  """Show the free response form for a funder and process it."""
  user = request.user
  event = Event.objects.get(pk=event_id)
  funder = CFAUser.objects.get(pk=funder_id)

  if request.method == 'POST':
    for key, value in request.POST.items():
      if key not in ('csrfmiddlewaretoken', 'save', 'submit'):
        # try to parse the question as a free response question
        # if that fails, try to parse it as a common free response question
        try:
          question = FreeResponseQuestion.objects.get(question=key)
        except FreeResponseQuestion.DoesNotExist:
          question = CommonFreeResponseQuestion.objects.get(question=key)
          try:
            answer = event.commonfreeresponseanswer_set.get(question=question)
          except CommonFreeResponseAnswer.DoesNotExist:
            event.commonfreeresponseanswer_set.create(question=question, answer=value)
          else:
            answer.answer = value
            answer.save()
        else:
          try:
            answer = event.freeresponseanswer_set.get(question=question)
          except FreeResponseAnswer.DoesNotExist:
            event.freeresponseanswer_set.create(question=question, answer=value)
          else:
            answer.answer = value
            answer.save()
      elif 'submit' in request.POST:
        event.notify_funder(funder)
        event.applied_funders.add(funder)
    # TODO: Change this to something meaningful
    return redirect(URL_ROOT)
  elif request.method == 'GET':
    form = FreeResponseForm(event_id, funder_id)
    return render_to_response('app/free-response-form.html',
                              {'form': form,
                              'event': event,
                              'funder': funder},
                              context_instance=RequestContext(request))
  else:
    return HttpResponseNotAllowed(['GET', 'POST'])


def funders(request, event_id):
  """List all the funders."""
  fs = CFAUser.objects.filter(user_type='F')
  event = Event.objects.get(id=event_id)
  funder_dict = dict()
  for funder in fs:
    funder_dict[funder] = {'id': funder.id,
      'willing': funder.is_willing_to_fund(event), 
      'applied': funder in event.applied_funders.all()}
  return render_to_response('app/eligible-funders.html', {'funders': funder_dict,
                            'event': event}, 
                            context_instance=RequestContext(request))
def application(request):
  # test data
  FunderItem = namedtuple('FunderItem', ['name', 'desc', 'question'])
  test_funders = [
    FunderItem(
      name="ORGANIZATION 1",
      desc="MISSION: Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
      question="How much do you want my money? Why? Please explain."
    ),
    FunderItem(
      name="ORGANIZATION 2",
      desc="MISSION: Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
      question="What is the meaning of life?"
    ),
    FunderItem(
      name="ORGANIZATION 3",
      desc="MISSION: Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
      question="How much do you want my money? Why? Please explain."
    ),
  ]
  
  # prepare funder-qs dict
  funder_qs = {}
  for idx, f in enumerate(test_funders):
    if f.question in funder_qs:
      funder_qs[f.question][0] += " funder-q-"+str(idx)
      funder_qs[f.question][1] += ", "+f.name
    else:
      funder_qs[f.question] = [
        "funder-q-"+str(idx),
        f.name
      ]
  
  return render_to_response('app/application.html',
                            {'test_funders': test_funders,
                             'funder_qs': funder_qs,
                            },
                            context_instance=RequestContext(request))


def submitted(request, sha):
  """Render submitted applications suitable for sharing among funders."""
  user = request.user
  event = Event.objects.get(pk=event_id)
  if request.method == 'GET':
    form = EventForm(event)
    if user.cfauser.is_funder:
      for key in form.fields:
        form.fields[key].widget.attrs['disabled'] = True
      other_form = FreeResponseForm(event_id, user.cfauser.id)
      for key in other_form.fields:
        other_form.fields[key].widget.attrs['disabled'] = True
    else:
      other_form = None
    return render_to_response('app/event-edit.html',
      {'form': form, 'event': event, 'is_funder':user.cfauser.is_funder,
      'other_form': other_form, 'funder_id':user.cfauser.id,
      'cfauser_id': user.cfauser.id},
      context_instance=RequestContext(request))
  else:
    return HttpResponseNotAllowed(['GET'])

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

def save_items(event, request):
  item_names = request.POST.getlist('item_name')
  item_quantity = request.POST.getlist('item_quantity')
  item_price_per_unit = request.POST.getlist('item_price_per_unit')
  item_funding = request.POST.getlist('item_funding_already_received')
  item_category = request.POST.getlist('item_category')
  event.item_set.all().delete()
  for name, quantity, price_per_unit,funding, cat in zip(item_names,item_quantity,item_price_per_unit,item_funding, item_category):
    event.item_set.create(name=name, quantity=quantity, price_per_unit=price_per_unit, funding_already_received=funding, category='F')

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
