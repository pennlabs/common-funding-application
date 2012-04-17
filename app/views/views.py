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
    event = Event.objects.get(pk=event_id)
    try:
      key = request.GET['key']
    except KeyError:
      user = request.user.get_profile()
      if user.is_funder or user.requested(event):
        return view(request, event_id, *args, **kwargs)
    else:
      if key == event.secret_key:
        return view(request, event_id, *args, **kwargs)
      else:
        return redirect(NOT_AUTHORIZED)
  return protected_view


def requester_only(view):
  """Ensure only the user who requested the event can access a page."""
  def protected_view(request, event_id, *args, **kwargs):
    user = request.user.get_profile()
    event = Event.objects.get(pk=event_id)
    if user.is_requester and user.requested(event):
      return view(request, event_id, *args, **kwargs)
    else:
      return redirect(NOT_AUTHORIZED)
  return protected_view


@login_required
def events(request):
  if request.method == 'GET':
    user = request.user
    if user.get_profile().is_requester:
      apps = Event.objects.filter(requester=user.get_profile()).extra(order_by=['date'])
    else: #TODO: filter for funders once submitting functionality has been implemented
      apps = user.get_profile().event_applied_funders.all().extra(order_by=['date'])
    return render_to_response('app/events.html',
                              {'apps': apps},
                              context_instance=RequestContext(request))
  else:
    return HttpResponseNotAllowed(['GET'])


@login_required
def event_new(request):
  """Form to create a new event."""
  if request.method == 'POST':
    event = Event.objects.create(
                            name=request.POST['name'],
                            date=request.POST['date'],
                            requester=request.user.get_profile(),
                            location=request.POST['location'],
                            organizations=request.POST['organizations']
                          )   
    event.save_from_form(request.POST)
    return redirect('app.views.events')
  elif request.method == 'GET':
    return render_to_response('app/application-requester.html',
        context_instance=RequestContext(request))
  else:
    return HttpResponseNotAllowed(['GET'])


@login_required
@requester_only
def event_edit(request, event_id):
  user = request.user
  if request.method == 'POST':
    event = Event.objects.get(pk=event_id)
    event.date = request.POST['date']
    event.name = request.POST['name']
    event.organizations = request.POST['organizations']
    event.location = request.POST['location']
    event.save()
    event.save_from_form(request.POST)
    return redirect('app.views.events')
  elif request.method == 'GET':
    event = Event.objects.get(pk=event_id)

    # can't get the event's funders?
    return render_to_response('app/application-requester.html',
        {
          'event': event
        },
        context_instance=RequestContext(request))
  else:
    return HttpResponseNotAllowed(['GET'])


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
                                              defaults={'amount': 0})
          amount_funded = sum(grant.amount for grant in 
              Grant.objects.filter(item=item))
          amount_funded += item.funding_already_received

          # if the funder gave too much, adjust the price to be only enough
          if amount + amount_funded - grant.amount > item.total:
            amount = item.total - amount_funded + grant.amount

          grant.amount = amount
          grant.save()

          grants.append(grant)

        #if grants:
          # email the event requester indicating that they've been funded
          #event.notify_requester(grants)
          #funder.notify_osa(event, grants)
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

    # can't get the event's funders?
    return render_to_response('app/application-funder.html',
        {
          'event': event,
        },
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


@login_required
@requester_only
def event_destroy(request, event_id):
  event = Event.objects.get(pk=event_id)
  event.delete()
  return redirect('app.views.events')
