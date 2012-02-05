from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.forms import Form
from django.forms.fields import CharField, ChoiceField, DecimalField
from django.forms.widgets import RadioSelect
from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from models import Event, Question


YES_OR_NO = (
    ('Y', 'Yes'),
    ('N', 'No'),
)

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
        return render_to_response('index.html',
                                  context_instance=RequestContext(request))

def login(request):
    username = request.POST['user']
    password = request.POST['pass']
    user = authenticate(username=username, password=password)
    if user is not None:
        auth_login(request, user)
        return redirect('app.views.apps_list')
    else:
        return redirect('app.views.index')

def logout(request):
    auth_logout(request)
    return redirect('app.views.index')

def questionnaire(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)
        if request.method == 'POST':
            for (key, value) in request.POST.items():
                if key != 'csrfmiddlewaretoken':
                    question = Question.objects.get(question=key)
                    try:
                        answer = event.answer_set.get(question=question)
                        answer.answer = value
                        answer.save()
                    except Answer.DoesNotExist:
                        event.answer_set.create(question=question,
                                                answer=value)
            return HttpResponseRedirect('/')

        else:
            form = QuestionnaireForm(event)
    
        return render_to_response('questionnaire.html',
                                  {'form' : form, 'event_id' : event_id},
                                  context_instance=RequestContext(request)
                                 )

    except Event.DoesNotExist:
        return render_to_response('error.html')
    
def apps_list(request):
    if request.user.is_authenticated():
        apps = Event.objects.all()
        return render_to_response('applist.html',
                                  {'apps': apps,
                                   'user': request.user.cfauser,})
    else:
        return redirect('app.views.index')

def form(request):
    return render_to_response('form-requester.html')
