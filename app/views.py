import os

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.forms import Form
from django.forms.fields import CharField, ChoiceField, DateField, DecimalField
from django.forms.widgets import DateInput, RadioSelect
from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

from models import Event, EligibilityQuestion, EligibilityAnswer
from sandbox_config import URL_ROOT


YES_OR_NO = (
  ('Y', 'Yes'),
  ('N', 'No'),
)


class EventForm(Form):
  def __init__(self, event_id, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)
    self.fields['name'] = CharField(max_length=256)
    self.fields['date'] =\
        DateField(widget=DateInput(attrs={'class': 'datepicker'}))
    for question in EligibilityQuestion.objects.all():
      self.fields[unicode(question)] =\
        ChoiceField(widget=RadioSelect, choices=YES_OR_NO)
    try:
      event = Event.objects.get(pk=event_id)
      self.initial['name'] = event.name
      self.initial['date'] = event.date
      for answer in event.eligibilityanswer_set.all():
        self.initial[unicode(answer.question)] = answer.answer
    except Event.DoesNotExist:
      pass


class EligibilityQuestionnaireForm(Form):
  def __init__(self, event, *args, **kwargs):
    super(EligibilityQuestionnaireForm, self).__init__(*args, **kwargs)
    for question in EligibilityQuestion.objects.all():
      self.fields[unicode(question)] = \
        ChoiceField(widget=RadioSelect, choices=YES_OR_NO)
    for answer in event.eligibilityanswer_set.all():
      self.initial[unicode(answer.question)] = answer.answer


class BudgetForm(Form):
  def __init__(self, event, *args, **kwargs):
    super(BudgetForm, self).__init__(*args, **kwargs)
    items = event.item_set.all()
    for index, item in enumerate(items, start=1):
      self.fields["Item %d", index] = CharField(max_length=256)
      self.fields["Amount %d", index] = \
        DecimalField(max_digits=17, decimal_places=2)
      self.initial["Item %d", index] = item.description
      self.initial["Amount %d", index] = item.amount
    
    self.fields["Item %d", len(items) + 1] = CharField(max_length=256)
    self.fields["Amount %d", len(items) + 1] = \
      DecimalField(max_digits=17, decimal_places=2)


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


def modify_event(request):
  user = request.user
  if user.is_authenticated():
    
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

  else:
    return redirect(URL_ROOT)  

  
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
                                  {'error_message' : "Unable to modify event"},
                                  context_instance=RequestContext(request))
      if user.cfauser != event.requester:
        return render_to_response('error.html',
                                  {'error_message' : "You do not have permission to modify this event"},
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
                                  {'error_message' : "Unable to view event"},
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
  # test code
  fundDict = {'SAC': 800, 'SCUE': 500, 'APSC': 100}
  fundTotalAmount = 2000
	
  return render_to_response('itemlist-funder.html',
                            {'fundDict': fundDict,
                             'fundTotalAmount': fundTotalAmount},
                            context_instance=RequestContext(request))


def delete_event(request):
  try:
    event = Event.objects.get(pk=request.GET['event_id'])
    event.delete()
    return redirect(os.path.join(URL_ROOT, 'apps'))
  except Event.DoesNotExist:
    return redirect(os.path.join(URL_ROOT, 'error'))


def error(request):
  return render_to_response('error.html',
                            context_instance=RequestContext(request))


def funders(request):
  return render_to_response('eligible-funders.html',
                            context_instance=RequestContext(request))
