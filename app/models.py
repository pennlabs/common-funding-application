import sha

from collections import namedtuple
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import dispatcher, receiver


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
  osa_email = models.EmailField() # The e-mail of the contact in OSA

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
    def grants(self):
      EventGrant = namedtuple('EventGrant', 'item currentAmount totalAmount grants')
      for item in self.item_set.all():
        grants = Grant.objects.filter(item=item)
        item_grants = dict((grant.funder, grant.amount) for grant in grants)
        yield EventGrant(item=item,
            currentAmount=sum(int(v) for v in item_grants.itervalues()),
            totalAmount=item.amount,
            grants=item_grants)

    @property
    def secret_key(self):
      """Unique key that can be shared so that anyone can view the event."""
      return sha.new("".join([self.name, str(self.date), str(self.requester)])).hexdigest()

    def __unicode__(self):
        return "%s: %s, %s" % (unicode(self.requester),
                               self.name,
                               self.date.isoformat())

    class Meta:
        unique_together = ("name", "date", "requester")


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
