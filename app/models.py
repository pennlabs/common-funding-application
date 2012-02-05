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

    def is_funder(self):
        return self.user_type == 'F'

    def is_requester(self):
        return self.user_type == 'R'

class Event(models.Model):
    name = models.CharField(max_length=256)
    date = models.DateField()
    requester = models.ForeignKey(CFAUser)

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

class Answer(models.Model):
    question = models.ForeignKey(Question)
    event = models.ForeignKey(Event)
    answer = models.CharField(max_length=1, choices=YES_OR_NO)

    def __unicode__(self):
        return unicode(self.question) + " " + self.answer

    class Meta:
        unique_together = ("question", "event", "answer")
    
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
        return unicode(self.item) + ", " + unicode(self.funder) + ", " + self.amount

    class Meta:
        unique_together = ("funder", "item")

class FunderConstraint(models.Model):
    funder = models.ForeignKey(CFAUser)
    question = models.ForeignKey(Question)
    answer = models.CharField(max_length=1, choices=YES_OR_NO)
    
    def __unicode__(self):
        return unicode(self.funder) + ", " + unicode(self.question) + ": " + self.answer

    class Meta:
        unique_together = ("funder", "question")
