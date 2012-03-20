from collections import namedtuple
from django.contrib.auth.models import User
from django.db import models


YES_OR_NO = (
    ('Y', 'YES'),
    ('N', 'NO'),
)

REQUESTER_OR_FUNDER = (
    ('R', 'REQUESTER'),
    ('F', 'FUNDER'),
)


class CFAUser(models.Model):
    user = models.OneToOneField(User)
    user_type = models.CharField(max_length=1,
                                 choices=REQUESTER_OR_FUNDER)

    def __unicode__(self):
        return unicode(self.user)

    @property
    def is_funder(self):
        return self.user_type == 'F'

    @property
    def is_requester(self):
        return not self.is_funder

    def is_willing_to_fund(self, event):
        for constraint in self.funderconstraint_set.all():
            event_answer = event.eligibilityanswer_set.get(question=
                constraint.question).answer
            if not event_answer == constraint.answer:
                return False
        return True

      


class Event(models.Model):
    name = models.CharField(max_length=256)
    date = models.DateField()
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


    def __unicode__(self):
        return "%s: %s, %s" % (unicode(self.requester),
                               self.name,
                               self.date.isoformat())

    class Meta:
        unique_together = ("name", "date", "requester")


class EligibilityQuestion(models.Model):
    question = models.TextField()
    
    def __unicode__(self):
        return self.question


class EligibilityAnswer(models.Model):
    question = models.ForeignKey(EligibilityQuestion)
    event = models.ForeignKey(Event)
    answer = models.CharField(max_length=1, choices=YES_OR_NO)

    def __unicode__(self):
        return "%s %s" % (unicode(self.question), self.answer)

    class Meta:
        unique_together = ("question", "event", "answer")


class FreeResponseQuestion(models.Model):
    question = models.TextField()
    funder = models.ForeignKey(CFAUser)

    def __unicode__(self):
        return unicode(self.question)


class FreeResponseAnswer(models.Model):
    question = models.ForeignKey(FreeResponseQuestion)
    event = models.ForeignKey(Event)
    answer = models.TextField()
    
    def __unicode__(self):
        return "%s %s" % (unicode(self.question), self.answer)


class Item(models.Model):
    event = models.ForeignKey(Event)
    description = models.CharField(max_length=256)
    amount = models.DecimalField(max_digits=17, decimal_places=2)

    def __unicode__(self):
        return self.description


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
