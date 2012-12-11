import os
from decimal import Decimal
from collections import namedtuple
from datetime import datetime
import json

import smtplib
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string

from sandbox_config import URL_ROOT

from app.models import Event, EligibilityQuestion, EligibilityAnswer, \
    FreeResponseQuestion, FreeResponseAnswer, Grant, CFAUser, \
    CommonFreeResponseQuestion, CommonFreeResponseAnswer, Comment


NOT_AUTHORIZED = 'app.views.events'

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
      if request.user.is_staff or user.is_funder or user.requested(event):
        return view(request, event_id, *args, **kwargs)
      else:
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
    user = request.user.get_profile()
    event = Event.objects.get(pk=event_id)
    if user.is_requester and user.requested(event):
      return view(request, event_id, *args, **kwargs)
    else:
      return redirect(NOT_AUTHORIZED)
  return protected_view

# GET  /
@login_required
def events(request):
  if request.method == 'GET':
    user = request.user
    cfauser = user.get_profile()
    if user.is_staff:
      apps = Event.objects.order_by('date')
    elif cfauser.is_requester:
      apps = Event.objects.filter(requester=cfauser).order_by('date')
    else: # cfauser.is_funder
      apps = cfauser.event_applied_funders.exclude(status=Event.SAVED).order_by('date')
    return render_to_response('app/events.html',
                              {'apps': apps},
                              context_instance=RequestContext(request))
  else:
    return HttpResponseNotAllowed(['GET'])

# GET  /new
# POST /new
@login_required
def event_new(request):
  """Form to create a new event."""
  if request.method == 'POST':
    POST = request.POST
    name = POST['name']
    status = Event.SAVED if 'save' in POST else Event.SUBMITTED
    time, date = [POST.get('time', None), POST.get('date', None)]
    if bool(date):
      date = datetime.strptime(date,'%m/%d/%Y')
    else:
      date = datetime.now()
    if not bool(time):
      time = datetime.now()
    admission_fee = POST['admissionfee'] if bool(POST['admissionfee']) else 0
    anticipated_attendance = POST['anticipatedattendance'] if bool(POST['anticipatedattendance']) else 0
    funding_already_received = POST['fundingalreadyreceived'] if bool(POST['fundingalreadyreceived']) else 0
    event = Event.objects.create(
                            status=status,
                            name=name,
                            date=date,
                            requester=request.user.get_profile(),
                            location=POST['location'],
                            organizations=POST['organizations'],
                            contact_email=POST['contactemail'],
                            time=time,
                            contact_phone=POST['contactphone'],
                            anticipated_attendance=anticipated_attendance,
                            admission_fee=admission_fee,
                            advisor_email=POST['advisoremail'],
                            advisor_phone=POST['advisorphone'],
                            funding_already_received=funding_already_received
                          )
    event.save_from_form(POST)
    # need to move this up in order to not save the event
    if not bool(name):
      messages.error(request, "Please provide a name for the event")
      return render_to_response('app/application-requester.html',
          {'event': event},
          context_instance=RequestContext(request))
    if status is Event.SAVED:
      message = 'Saved application for %s' % event.name
    else:
      funders = event.applied_funders.all()
      length = len(funders)
      plural = "funder" if length == 1 else "funders"
      message = 'Submitted application for %s to %d %s' % (event.name, length, plural)
      for funder in funders:
        event.notify_funder(funder)
    messages.success(request, message)
    return redirect('app.views.events')
  elif request.method == 'GET':
    return render_to_response('app/application-requester.html',
        context_instance=RequestContext(request))
  else:
    return HttpResponseNotAllowed(['GET'])

# GET  /1/edit
# POST /1/edit
@login_required
@requester_only
def event_edit(request, event_id):
  user = request.user
  event = Event.objects.get(pk=event_id)
  if event.funded or event.submitted:
    return redirect('app.views.event_show', event_id)
  if request.method == 'POST':
    status = Event.SAVED if 'save' in request.POST else Event.SUBMITTED
    event.status = status
    event.name = request.POST['name']
    event.date = datetime.strptime(request.POST['date'],'%m/%d/%Y')
    event.organizations = request.POST['organizations']
    event.location = request.POST['location']
    event.time = request.POST['time']
    event.contact_email = request.POST['contactemail']
    event.contact_phone = request.POST['contactphone']
    event.anticipated_attendance = request.POST['anticipatedattendance']
    event.admission_fee = request.POST['admissionfee']
    event.advisor_email = request.POST['advisoremail']
    event.advisor_phone = request.POST['advisorphone']
    event.funding_already_received = request.POST['fundingalreadyreceived']
    event.save()
    event.save_from_form(request.POST)
    if status is Event.SAVED:
      message = 'Saved application for %s' % event.name
    else:
      funders = event.applied_funders.all()
      message = 'Submitted application for %s to %d funders' % (event.name, len(funders))
      for funder in funders:
        event.notify_funder(funder)
    messages.success(request, message)
    return redirect('app.views.events')
  elif request.method == 'GET':
    return render_to_response('app/application-requester.html',
        {'event': event},
        context_instance=RequestContext(request))
  else:
    return HttpResponseNotAllowed(['GET'])

# GET  /1
# POST /1
@authorization_required
def event_show(request, event_id):
  user = request.user
  event = Event.objects.get(pk=event_id)
  if request.method == 'POST': #TODO: should really be PUT
    if user.get_profile().is_funder:
      grants = []
      for item in event.item_set.all():
        amount = request.POST.get("item_" + str(item.id), None)
        if amount:
          amount = Decimal(amount)
          grant, _ = Grant.objects.get_or_create(funder=user.get_profile(),
                                              item=item,
                                              defaults={'amount': 0})
          amount_funded = sum(grant.amount for grant in
                  Grant.objects.filter(item=item))
          amount_funded += item.funding_already_received
          # if the funder gave too much, adjust the price to be only enough
          if amount + amount_funded - grant.amount > item.total:
            amount = item.total - amount_funded + grant.amount
          # only append if the amount has changed
          if grant.amount != amount:
            grant.amount = amount
            grant.save()
            grants.append(grant)
      if grants:
        messages.success(request, "Saved grant!")
        # email the event requester indicating that they've been funded
        event.notify_requester(grants)
        event.status = Event.FUNDED
        event.save()
        # try to notify osa, but osa is not guaranteed to exist
        try:
          user.get_profile().notify_osa(event, grants)
        except smtplib.SMTPException:
          pass
      if request.POST.get('new-comment', None):
        comment = Comment(comment=request.POST['new-comment'],
          funder=user.get_profile(), event=event)
        comment.save()
      return redirect('app.views.events')
    else:
      return redirect('app.views.events')
  elif request.method == 'GET':
    return render_to_response('app/application-show.html',
        {'event': event},
        context_instance=RequestContext(request))
  else:
    return HttpResponseNotAllowed(['POST'])

# GET  /1/destroy
@login_required
@requester_only
def event_destroy(request, event_id):
  event = Event.objects.get(pk=event_id)
  event.delete()
  return HttpResponse(json.dumps({'event_id': event_id}), mimetype="application/json")
