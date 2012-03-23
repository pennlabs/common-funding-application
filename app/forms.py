from django.forms import Form, Textarea, ModelForm
from django.forms.fields import CharField, ChoiceField, DateField, DecimalField
from django.forms.widgets import DateInput, RadioSelect, TextInput

from models import Event, EligibilityQuestion, EligibilityAnswer, FreeResponseQuestion


YES_OR_NO = ( 
  ('Y', 'Yes'),
  ('N', 'No'),
)


class EventForm(ModelForm):

  class Meta:
    model = Event
    fields = ('name', 'date')
    # a required attribute is neccesary to make a field required
    # however, it doesn't need any value so we pass the empty string
    widgets = {
        'name': TextInput(attrs={'required': ''}),
        'date': DateInput(attrs={'required': '', 'class': 'datepicker'})
    }

  def __init__(self, event=None, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)
    for question in EligibilityQuestion.objects.all():
      self.fields[unicode(question)] = ChoiceField(
          widget=RadioSelect(attrs={'required': ''}),
            choices=YES_OR_NO)
    assert event is None or isinstance(event, Event), event
    if event:
      self.initial['name'] = event.name
      self.initial['date'] = event.date
      for answer in event.eligibilityanswer_set.all():
        self.initial[unicode(answer.question)] = answer.answer


class FreeResponseForm(Form):
  def __init__(self, event_id, funder_id, *args, **kwargs):
    super(FreeResponseForm, self).__init__(*args, **kwargs)
    questions = FreeResponseQuestion.objects.filter(funder__id=funder_id)
    for question in questions:
      self.fields[unicode(question)] = CharField(widget=Textarea)
    # populate answers from existing event if it exists
    try:
      event = Event.objects.get(pk=event_id)
      for answer in event.freeresponseanswer_set.all():
        self.initial[unicode(question)] = answer.answer
    except Event.DoesNotExist:
      pass


class FreeResponseSpecificationForm(Form):
  def __init__(self, funder_id, *args, **kwargs):
    super(FreeResponseForm, self).__init__(*args, **kwargs)
    questions = FreeResponseQuestions.objects.filter(funder__id=funder_id)
    for question in questions:
      self.fields[unicode(question)] = CharField(widget=forms.Textarea,
          initial=unicode(question))


class EligibilityQuestionnaireForm(Form):
  def __init__(self, event, *args, **kwargs):
    super(EligibilityQuestionnaireForm, self).__init__(*args, **kwargs)
    for question in EligibilityQuestion.objects.all():
      self.fields[unicode(question)] = ChoiceField(widget=RadioSelect, choices=YES_OR_NO)
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
