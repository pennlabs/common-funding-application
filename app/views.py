from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.forms import Form
from django.forms.fields import CharField, ChoiceField, DateField, DecimalField
from django.forms.widgets import DateInput, RadioSelect
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from models import Event, Question, Answer

from sandbox_config import *

YES_OR_NO = (
  ('Y', 'Yes'),
  ('N', 'No'),
)

class EventForm(Form):
  def __init__(self, event_id, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)
    self.fields['name'] = CharField(max_length=256)
    self.fields['date'] = DateField(widget=DateInput(attrs={'class':'datepicker'}))
    for question in Question.objects.all():
      self.fields[unicode(question)] =\
        ChoiceField(widget=RadioSelect, choices=YES_OR_NO)
    try:
      event = Event.objects.get(pk=event_id)
      self.initial['name'] = event.name
      self.initial['date'] = event.date
      for answer in event.answer_set.all():
        self.initial[unicode(answer.question)] = answer.answer
    except Event.DoesNotExist:
      pass

class QuestionnaireForm(Form):
  def __init__(self, event, *args, **kwargs):
    super(QuestionnaireForm, self).__init__(*args, **kwargs)
    for question in Question.objects.all():
      self.fields[unicode(question)] = \
        ChoiceField(widget=RadioSelect, choices=YES_OR_NO)
    for answer in event.answer_set.all():
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
    return redirect('app.views.apps_list')
  else:
    return redirect('app.views.login')
    #return render_to_response('index.html',
    #                          context_instance=RequestContext(request))

def login(request):
  if request.method == 'POST':
    username = request.POST['user']
    password = request.POST['pass']
    user = authenticate(username=username, password=password)
    if user is not None:
      auth_login(request, user)
      return redirect('app.views.apps_list')
    else:
      return render_to_response('login.html',
                                {'login_failed' : True},
                                context_instance=RequestContext(request))
  else:
    return render_to_response('login.html',
                              context_instance=RequestContext(request))

def logout(request):
  auth_logout(request)
  return redirect('app.views.index')

def modify_event(request):
  try:
    if request.method == 'POST':
      event_id = request.POST.get('event_id', None)
      if event_id:
        event = Event.objects.get(pk=event_id)
      else:
        event = Event.objects.create(name=request.POST['name'], date=request.POST['date'], requester=request.user.cfauser)
      for (key, value) in request.POST.items():
        if key != 'csrfmiddlewaretoken' and key != 'event_id':
          if key == 'name':
            event.name = value
            event.save()
          elif key == 'date':
            event.date = value
            event.save()
          else:
            question = Question.objects.get(question=key)
            try:
              answer = event.answer_set.get(question=question)
              answer.answer = value
              answer.save()
            except Answer.DoesNotExist:
              event.answer_set.create(question=question,
                          answer=value)
      return redirect('app.views.apps_list')

    else:
      event_id = request.GET.get('event_id', None)
      form = EventForm(event_id)
  
    return render_to_response('event-form.html',
                  {'form' : form, 'event_id' : event_id},
                  context_instance=RequestContext(request)
                 )

  except Event.DoesNotExist:
    return redirect('app.views.error')
  

def questionnaire(request):
  try:
    if request.method == 'POST':
      event_id = request.POST['event_id']
      event = Event.objects.get(pk=event_id)
      for (key, value) in request.POST.items():
        if key != 'csrfmiddlewaretoken' and key != 'event_id':
          question = Question.objects.get(question=key)
          try:
            answer = event.answer_set.get(question=question)
            answer.answer = value
            answer.save()
          except Answer.DoesNotExist:
            event.answer_set.create(question=question,
                        answer=value)
      return redirect('app.views.apps_list')

    else:
      event_id = request.GET['event_id']
      event = Event.objects.get(pk=event_id)
      form = QuestionnaireForm(event)
  
    return render_to_response('questionnaire.html',
                  {'form' : form, 'event_id' : event_id},
                  context_instance=RequestContext(request)
                 )

  except Event.DoesNotExist:
    return render_to_response('error.html')
  
def apps_list(request):
  user = request.user
  if user.is_authenticated():
    if user.cfauser.is_requester():
      apps = Event.objects.filter(requester=user.cfauser)
    else:
      apps = Event.objects.all()
    return render_to_response('applist.html',
                  {'apps': apps,
                   'user': user.cfauser,})
  else:
    return redirect('app.views.index')

def form(request):
  return render_to_response('form-requester.html')

def itemlist(request):
  return render_to_response('itemlist.html')

def itemlist_funder(request):
	# test code
	fundDict = {'SAC': 800, 'SCUE': 500, 'APSC': 100}
	fundTotalAmount = 2000
	
	return render_to_response('itemlist-funder.html',
														{'fundDict': fundDict,
														 'fundTotalAmount': fundTotalAmount})

def delete_event(request):
  try:
    event = Event.objects.get(pk=request.GET['event_id'])
    event.delete()
    return redirect('app.views.apps_list')
  except Event.DoesNotExist:
    return redirect('app.views.error')

def error(request):
  return render_to_response('error.html')
