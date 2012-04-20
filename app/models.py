from collections import namedtuple
import re
import sha

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import dispatcher, receiver
from django.template.loader import render_to_string


YES_OR_NO = (
    ('Y', 'YES'),
    ('N', 'NO'),
)

REQUESTER_OR_FUNDER = (
    ('R', 'REQUESTER'),
    ('F', 'FUNDER'),
)


class CFAUser(models.Model):
  """
  A CFA User profile.

  # Create user
  >>> u = User.objects.create_user("alice", "alice@example.com", "1234")
  >>> cfau = u.get_profile()
  >>> cfau.is_requester
  True
  >>> cfau.is_funder
  False
  """
  user = models.OneToOneField(User)
  user_type = models.CharField(max_length=1,
                               choices=REQUESTER_OR_FUNDER)
  osa_email = models.EmailField(null=True) # The e-mail of the contact in OSA
  mission_statement = models.TextField(max_length=256)

  def __unicode__(self):
      return unicode(self.user)

  @property
  def is_funder(self):
      return self.user_type == 'F'

  @property
  def is_requester(self):
      return not self.is_funder

  def is_willing_to_fund(self, event):
    """Check if a funder is willing to fund an event."""
    assert self.is_funder
    for constraint in self.funderconstraint_set.all():
        event_answer = event.eligibilityanswer_set.get(question=
            constraint.question).answer
        if not event_answer == constraint.answer:
            return False
    return True

  def requested(self, event):
    """Check if a user requested an event."""
    assert self.is_requester
    return self == event.requester

  def notify_osa(self, event, grants):
    """Notify OSA that an event has been funded."""
    assert self.is_funder
    context = {'funder': self, 'event': event, 'grants': grants}
    subject = render_to_string('app/osa_email_subject.txt',
        context).strip()
    message = render_to_string('app/osa_email.txt', context)
    send_mail(subject, message, self.user.email, [str(self.osa_email)])


@receiver(sender=User, signal=post_save)
def create_profile(sender, instance, signal, created, **kwargs):
  """Create a CFAUser whenever a user is created."""
  if created:
    CFAUser.objects.create(user=instance, user_type='R')


class Event(models.Model):
    name = models.CharField(max_length=256)
    date = models.DateField()
    location = models.CharField(max_length=256)
    requester = models.ForeignKey(CFAUser, related_name='event_requester')
    organizations = models.CharField(max_length=256)

    applied_funders =\
        models.ManyToManyField(CFAUser,
                               related_name='event_applied_funders')

    @property
    def total_funds_already_received(self):
      """The total amount of money already received (before grants) for an event."""
      return sum(item.funding_already_received for item in self.item_set.all())

    @property
    def amounts(self):
      """Get a dictionary containing the amount each funder has granted."""
      amounts = dict((funder, 0) for funder in self.applied_funders.all())
      for item in self.item_set.all():
        for grant in item.grant_set.all():
          amounts[grant.funder] += grant.amount
      return amounts

    @property
    def total_funds_granted(self):
      """The total amount of money received via grants."""
      return sum(self.amounts.values())
    
    @property
    def funded(self):
      """Whether or not an event has been funded."""
      return self.total_funds_granted > 0

    @property
    def total_funds_received(self):
      """The total amount of money received (grants + pre grant)."""
      return self.total_funds_already_received + self.total_funds_granted

    @property
    def total_funds_requested(self):
      """The total amount of money requested for an event."""
      return sum(item.total for item in self.item_set.all())

    def save_from_form(self, POST):
      """Save an event from form data."""
      # save items
      names = POST.getlist('item_name')
      quantities = POST.getlist('item_quantity')
      prices_per_unit = POST.getlist('item_price_per_unit')
      funding_already_received = POST.getlist('item_funding_already_received')
      categories = POST.getlist('item_category')

      self.item_set.all().delete()
      for name, quantity, price, funding, cat in zip(names, quantities, prices_per_unit, funding_already_received, categories):
        # category defaults to F because we haven' implemented the different category choices
        if str(name) and str(quantity) and str(funding) and str(price):
          self.item_set.create(name=name, quantity=quantity,price_per_unit=price,funding_already_received=funding,category='F')

      # save questions

      # delete existing answers
      self.eligibilityanswer_set.all().delete()
      self.commonfreeresponseanswer_set.all().delete()
      
      # clear existing funders to re-add new ones
      self.applied_funders.clear()

      # create new answers and save funders
      # unchecked checkboxes will have neither answers nor funders associated with them
      for k, v in POST.items():
        if k.startswith('eligibility'):
          q_id = re.search("[0-9]+", k).group(0)
          question = EligibilityQuestion.objects.get(id=q_id)
          self.eligibilityanswer_set.create(question=question, event=self, answer='Y')
        elif k.startswith('commonfreeresponse'):
          q_id = re.search("[0-9]+", k).group(0)
          question = CommonFreeResponseQuestion.objects.get(id=q_id)
          self.commonfreeresponseanswer_set.create(question=question, event=self, answer=v)
        elif k.startswith('funder'):
          funder_id = re.search("[0-9]+", k).group(0)
          funder = CFAUser.objects.get(id=funder_id)
          self.applied_funders.add(funder)


    def notify_funder(self, funder):
      """Notify a funder that the requester has applied to them."""
      assert funder.is_funder
      context = {'requester': self.requester, 'event': self}
      subject = render_to_string('app/application_email_subject.txt',
          context).strip()
      message = render_to_string('app/application_email.txt', context)
      funder.user.email_user(subject, message)

    def notify_requester(self, grants):
      """Notify a requester that an event has been funded."""
      context = {'event': self, 'grants': self.grants}
      subject = render_to_string('app/grant_email_subject.txt',
          context).strip()
      message = render_to_string('app/grant_email.txt', context)
      self.requester.user.email_user(subject, message)


    @property
    def secret_key(self):
      """Unique key that can be shared so that anyone can view the event."""
      """To use the key append ?key=<key>"""
      return sha.new("".join([self.name, str(self.date), str(self.requester)])).hexdigest()

    @models.permalink
    def get_absolute_url(self):
      return ('app.views.event_show', [str(self.id)])

    def __unicode__(self):
        return "%s: %s, %s" % (unicode(self.requester),
                               self.name,
                               self.date.isoformat())

    class Meta:
        unique_together = ("name", "date", "requester")


class Comment(models.Model):
    """A comment, made by a funder, on an event application."""
    funder = models.ForeignKey(CFAUser)
    event = models.ForeignKey(Event)
    comment = models.TextField()

    def __unicode__(self):
        return self.comment


class Question(models.Model):
    question = models.TextField()
    
    def __unicode__(self):
        return self.question

    class Meta:
      abstract = True


class EligibilityQuestion(Question):
    pass


class EligibilityAnswer(models.Model):
    question = models.ForeignKey(EligibilityQuestion)
    event = models.ForeignKey(Event)
    answer = models.CharField(max_length=1, choices=YES_OR_NO)

    def __unicode__(self):
        return "%s %s" % (unicode(self.question), self.answer)

    class Meta:
        unique_together = ("question", "event", "answer")


class CommonFreeResponseQuestion(Question):
  """A free response question common to all funders."""
  pass


class CommonFreeResponseAnswer(models.Model):
  """An answer to a common free response question."""
  question = models.ForeignKey(CommonFreeResponseQuestion)
  event = models.ForeignKey(Event)
  answer = models.TextField()

  def __unicode__(self):
      return "%s %s" % (unicode(self.question), self.answer)


class FreeResponseQuestion(Question):
  """A unique free response question specified by a single funder."""
  funder = models.ForeignKey(CFAUser)


class FreeResponseAnswer(models.Model):
    question = models.ForeignKey(FreeResponseQuestion)
    event = models.ForeignKey(Event)
    answer = models.TextField()
    
    def __unicode__(self):
        return "%s %s" % (unicode(self.question), self.answer)


# TODO: Find the actual categories and update this
CATEGORIES = (
    ('F', 'FOOD'),
    ('D', 'DRINK'),
)


class Item(models.Model):
    """An item for an event."""
    event = models.ForeignKey(Event)
    name = models.CharField(max_length=256)
    # number of items
    quantity = models.IntegerField()
    # cost per item
    price_per_unit = models.DecimalField(max_digits=17, decimal_places=2)
    # funding already received before applications
    funding_already_received = models.DecimalField(max_digits=17, decimal_places=2)
    category = models.CharField(max_length=1, choices=CATEGORIES)

    @property
    def total(self):
      return self.price_per_unit * self.quantity

    def __unicode__(self):
        return self.name


class Grant(models.Model):
    funder = models.ForeignKey(CFAUser)
    item = models.ForeignKey(Item)
    amount = models.DecimalField(max_digits=17, decimal_places=2)

    def __unicode__(self):
        return "%s, %s, %d" % (unicode(self.item),
                               unicode(self.funder),
                               self.amount)

    class Meta:
        unique_together = ("funder", "item")


class FunderConstraint(models.Model):
    funder = models.ForeignKey(CFAUser)
    question = models.ForeignKey(EligibilityQuestion)
    answer = models.CharField(max_length=1, choices=YES_OR_NO)
    
    def __unicode__(self):
        return "%s, %s %s" % (unicode(self.funder),
                              unicode(self.question),
                              self.answer)

    class Meta:
        unique_together = ("funder", "question")
