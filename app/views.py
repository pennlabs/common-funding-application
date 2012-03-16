import os
from collections import namedtuple

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

from forms import EventForm, EligibilityQuestionnaireForm, BudgetForm, \
    FreeResponseForm
from models import Event, EligibilityQuestion, EligibilityAnswer, \
    FreeResponseQuestion, FreeResponseAnswer
from sandbox_config import URL_ROOT


def index(request):
  if request.user.is_authenticated():
    return redirect(os.path.join(URL_ROOT, 'apps'))
  else:
    return redirect(os.path.join(URL_ROOT, 'login'))


def login(request):
  if request.method == 'POST':
    username = request.POST['user']
    password = request.POST['pass']
    user = authenticate(username=username, password=password)
    if user is not None:
      auth_login(request, user)
      return redirect(os.path.join(URL_ROOT, 'apps'))
    else:
      return render_to_response('login.html',
                                {'login_failed': True},
                                context_instance=RequestContext(request))
  else:
    return render_to_response('login.html',
                              context_instance=RequestContext(request))


def logout(request):
  auth_logout(request)
  return redirect(URL_ROOT)


@login_required
def modify_event(request):
  user = request.user
  if request.method == 'POST':
    event_id = request.POST.get('event_id', None)
    
    try:
      if event_id:
        event = Event.objects.get(pk=event_id)
      else:
        event = Event.objects.create(name=request.POST['name'],
                                     date=request.POST['date'],
                                     requester=request.user.cfauser)
    except Event.DoesNotExist:
      return render_to_response('error.html',
                                {'error_message': "Invalid event id."},
                                context_instance=RequestContext(request))

    if user.cfauser != event.requester:
      return render_to_response('error.html',
                                {'error_message': "You are not authorized to edit this event"},
                                context_instance=RequestContext(request))

    for key, value in request.POST.items():
      if key != 'csrfmiddlewaretoken' and key != 'event_id':
        if key == 'name':
          event.name = value
          event.save()
        elif key == 'date':
          event.date = value
          event.save()
        else:
          question = EligibilityQuestion.objects.get(question=key)
          try:
            answer = event.eligibilityanswer_set.get(question=question)
            answer.answer = value
            answer.save()
          except EligibilityAnswer.DoesNotExist:
            event.eligibilityanswer_set.create(question=question,
                                    answer=value)
    return redirect(os.path.join(URL_ROOT, 'itemlist?event_id=' + str(event_id)))

  elif request.method == 'GET':
    event_id = request.GET.get('event_id', None)
    
    try:
      if event_id:
        event = Event.objects.get(pk=event_id)
        if user.cfauser.is_requester() and user.cfauser != event.requester:
          return render_to_response('error.html',
                                    {'error_message': "You are not authorized to view this event"},
                                    context_instance=RequestContext(request))

    except Event.DoesNotExist:
      return render_to_response('error.html',
                                {'error_message': "Invalid event"},
                                context_instance=RequestContext(request))


    form = EventForm(event_id)
    return render_to_response('event-form.html',
                              {'form': form, 'event_id': event_id},
                              context_instance=RequestContext(request))
  else:
    return HttpResponseNotAllowed(['GET', 'POST'])


def apps_list(request):
  user = request.user
  if user.is_authenticated():
    if user.cfauser.is_requester():
      apps = Event.objects.filter(requester=user.cfauser).extra(order_by=['date'])
    else: #TODO: filter for funders once submitting functionality has been implemented
      apps = Event.objects.all().extra(order_by=['date'])
    return render_to_response('applist.html',
                              {'apps': apps,
                               'user': user.cfauser,},
                              context_instance=RequestContext(request))
  else:
    return redirect(URL_ROOT)


def form(request):
  return render_to_response('form-requester.html',
                            context_instance=RequestContext(request))


def itemlist(request):
  user = request.user
  if user.is_authenticated():
    if request.method == 'POST':
      event_id = request.POST.get('event_id', None)
      try:
        event = Event.objects.get(pk=event_id)
      except Event.DoesNotExist:
        return render_to_response('error.html',
                                  {'error_message': "Unable to modify event"},
                                  context_instance=RequestContext(request))
      if user.cfauser != event.requester:
        return render_to_response('error.html',
                                  {'error_message': "You do not have permission to modify this event"},
                                  context_instance=RequestContext(request))
      item_names = request.POST.getlist('item_name')
      item_amounts = request.POST.getlist('item_amount')
      event.item_set.all().delete()
      for name, amount in zip(item_names, item_amounts):
        event.item_set.create(description=name, amount= amount)
      return redirect(os.path.join(URL_ROOT, 'apps'))
    
    elif request.method == 'GET':
      event_id = request.GET.get('event_id', None)
      try:
        event = Event.objects.get(pk=event_id)
        event_name = event.name
      except Event.DoesNotExist:
        return render_to_response('error.html',
                                  {'error_message': "Unable to view event"},
                                  context_instance=RequestContext(request))
      items = event.item_set.all()
      item_names = []
      item_amounts = []
      for item in items:
        item_names.append(str(item.description))
        item_amounts.append(str(item.amount))
      return render_to_response('itemlist.html',
                                {'event_id': event_id,
                                 'event_name': event_name,
                                 'items': zip(item_names, item_amounts),},
                                context_instance=RequestContext(request))
  
    else:
      return HttpResponseNotAllowed(['GET', 'POST'])

  else:
    return redirect(URL_ROOT)


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
      event_grants = []
      EventGrant = namedtuple('EventGrant', ['item', 'currentAmount', 'totalAmount', 'grants'])
      for item in event.item_set.all():
        grants = Grant.objects.filter(item=item)
        item_grants = {}
        for grant in grants:
          item_grants[grant.funder] = grant.amount
        event_grants.append(EventGrant(item=item,
                                       currentAmount=sum(int(v) for v in item_grants.itervalues()),
                                       totalAmount=item.amount,
                                       grants=item_grants))
    
    # test code, remove when you have test data
    #  event_grants.append(EventGrant(item=Item.objects.get(description='asdf'),
     #                                currentAmount=1400,
      #                               totalAmount=2000,
       #                              grants={'SAC': 800, 'SCUE': 500, 'APSC': 100}))

      return render_to_response('itemlist-funder.html',
                                {'event_grants': event_grants,
                                 'event_id': event_id},
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
      return redirect(os.path.join(URL_ROOT, 'apps'))
  else:
    return HttpResponseNotAllowed(['GET', 'POST'])


def delete_event(request):
  try:
    event = Event.objects.get(pk=request.GET['event_id'])
    event.delete()
    return redirect(os.path.join(URL_ROOT, 'apps'))
  except Event.DoesNotExist:
    return redirect(os.path.join(URL_ROOT, 'error'))


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
  if user.cfauser != event.requester:
    return render_to_response('error.html',
        {'error_message': "You: %s Requester: %s" % (user.cfauser, event.requester)},
                              context_instance=RequestContext(request))
  if request.method == 'POST':
    for key, value in request.POST.items():
      if key not in ('csrfmiddlewaretoken', 'event_id', 'funder_id'):
        question = FreeResponseQuestion.objects.get(question=key)
        # update answer if it exists or make a new answer
        try:
          answer = event.freeresponseanswer_set.get(question=question)
          answer.answer = value
          answer.save()
        except FreeResponseAnswer.DoesNotExist:
          event.freeresponseanswer_set.create(question=question,
                                  answer=value)
    # TODO: Change this to something meaningful
    return redirect(URL_ROOT)
  elif request.method == 'GET':
    form = FreeResponseForm(event_id, funder_id)
    return render_to_response('free-response-form.html',
                              {'form': form, 'event_id': event_id, 'funder_id': funder_id},
                              context_instance=RequestContext(request))
  else:
    return HttpResponseNotAllowed(['GET', 'POST'])


def error(request):
  return render_to_response('error.html',
                            context_instance=RequestContext(request))


def funders(request):
  return render_to_response('eligible-funders.html',
                            context_instance=RequestContext(request))
