import os
from collections import namedtuple

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

from forms import EventForm, EligibilityQuestionnaireForm, BudgetForm, \
    FreeResponseForm
from models import Event, EligibilityQuestion, EligibilityAnswer, \
    FreeResponseQuestion, FreeResponseAnswer, Grant, CFAUser
from sandbox_config import URL_ROOT


def index(request):
    return redirect('app.views.events')


def authorization_required(view):
  def protected_view(request, event_id, *args, **kwargs):
    user = request.user
    event = Event.objects.get(pk=event_id)
    if user.cfauser.requested(event):
      return view(request, event_id, *args, **kwargs)
    else:
      return HttpResponse(status=401) # not authorized
  return protected_view


@login_required
def events(request):
  if request.method == 'POST':
    event = Event.objects.create(name=request.POST['name'],
                                 date=request.POST['date'],
                                 requester=request.user.cfauser)
    return redirect('app.views.items', event_id)
  elif request.method == 'GET':
    user = request.user
    if user.cfauser.is_requester:
      apps = Event.objects.filter(requester=user.cfauser).extra(order_by=['date'])
    else: #TODO: filter for funders once submitting functionality has been implemented
      apps = user.cfauser.event_applied_funders.all().extra(order_by=['date'])
    return render_to_response('events.html',
                              {'apps': apps,
                               'user': user.cfauser,},
                              context_instance=RequestContext(request))
  else:
    return HttpResponseNotAllowed(['GET', 'POST'])


@login_required
def event_new(request):
  pass


@login_required
@authorization_required
def event_show(request, event_id):
  user = request.user
  if request.method == 'POST': #TODO: should really be PUT
    event = Event.objects.get(pk=event_id)

    for key, value in request.POST.items():
      if key in ('csrfmiddlewaretoken', 'event_id'):
        continue
      if key == 'name':
        event.name = value
      elif key == 'date':
        event.date = value
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
  else:
    return HttpResponseNotAllowed(['POST'])


@login_required
@authorization_required
def answers(request, event_id):
  user = request.user
  if request.method == 'GET':
    try:
      event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
      return render_to_response('error.html',
                                {'error_message': "Invalid event"},
                                context_instance=RequestContext(request))

    form = EventForm(event_id)
    return render_to_response('event-form.html',
                              {'form': form,
                              'event': event},
                              context_instance=RequestContext(request))
  else:
    return HttpResponseNotAllowed(['GET'])


def form(request):
  return render_to_response('form-requester.html',
                            context_instance=RequestContext(request))


@login_required
@authorization_required
def items(request, event_id):
  user = request.user
  if request.method == 'POST':
    event_id = request.POST.get('event_id', None)
    event = Event.objects.get(pk=event_id)
    item_names = request.POST.getlist('item_name')
    item_amounts = request.POST.getlist('item_amount')
    event.item_set.all().delete()
    for name, amount in zip(item_names, item_amounts):
      event.item_set.create(description=name, amount= amount)
    return redirect('app.views.funders', event_id)
  elif request.method == 'GET':
    event = Event.objects.get(pk=event_id)
    return render_to_response('itemlist.html',
                              {'event': event},
                              context_instance=RequestContext(request))
  else:
    return HttpResponseNotAllowed(['GET', 'POST'])


def itemlist_funder(request):
  user = request.user
  if user.is_authenticated():
    if request.method == 'GET':
      event_id = request.GET.get('event_id', None)
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
@authorization_required
def event_destroy(request, event_id):
  event = Event.objects.get(pk=event_id)
  event.delete()
  return redirect('app.views.events')


@login_required
def free_response(request):
  user = request.user

  # ensure event exists
  event_id = request.GET.get('event_id', None) or request.POST.get('event_id', None)
  if event_id is None:
    return render_to_response('error.html',
                              {'error_message': "No event id specified."},
                              context_instance=RequestContext(request))
  try:
    event = Event.objects.get(pk=event_id)
  except Event.DoesNotExist:
    return render_to_response('error.html',
                              {'error_message': "Invalid event id."},
                              context_instance=RequestContext(request))

  # ensure funder_id is specified
  funder_id = request.GET.get('funder_id', None) or request.POST.get('funder_id', None)
  if funder_id is None:
    return render_to_response('error.html',
                              {'error_message': "No funder id specified."},
                              context_instance=RequestContext(request))
  if request.method == 'POST':
    if user.cfauser != event.requester:
      return render_to_response('error.html',
        {'error_message': "You: %s Requester: %s" % (user.cfauser, event.requester)},
        context_instance=RequestContext(request))
    for key, value in request.POST.items():
      if key not in ('csrfmiddlewaretoken', 'event_id', 'funder_id', 'save', 
        'submit'):
        question = FreeResponseQuestion.objects.get(question=key)
        # update answer if it exists or make a new answer
        try:
          answer = event.freeresponseanswer_set.get(question=question)
          answer.answer = value
          answer.save()
        except FreeResponseAnswer.DoesNotExist:
          event.freeresponseanswer_set.create(question=question,
                                  answer=value)
      elif 'submit' in request.POST:
        event.applied_funders.add(CFAUser.objects.get(id=funder_id))
    # TODO: Change this to something meaningful
    return redirect(URL_ROOT)
  elif request.method == 'GET':
    form = FreeResponseForm(event_id, funder_id)
    return render_to_response('free-response-form.html',
                              {'form': form, 'event_id': event_id,
                              'funder_id': funder_id,
                              'is_funder': user.cfauser.is_funder},
                              context_instance=RequestContext(request))
  else:
    return HttpResponseNotAllowed(['GET', 'POST'])


def error(request):
  return render_to_response('error.html',
                            context_instance=RequestContext(request))


def funders(request, event_id):
  """List all the funders."""
  fs = CFAUser.objects.filter(user_type='F')
  event = Event.objects.get(id=event_id)
  funder_dict = dict()
  for funder in fs:
    funder_dict[funder.user.username] = {'id': funder.id,
      'willing': funder.is_willing_to_fund(event), 
      'applied': funder in event.applied_funders.all()}
  return render_to_response('eligible-funders.html', {'funders': funder_dict,
                            'event_id': event_id}, 
                            context_instance=RequestContext(request))
