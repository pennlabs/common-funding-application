from django.contrib.auth.models import User
from django.db import models


class Requester(models.Model):
    user = models.ForeignKey(User)

class Funder(models.Model):
    user = models.ForeignKey(User)

class Question(models.Model):
    content = models.TextField()
    format = models.CharField(max_length=16)

class Application(models.Model):
    requester = models.ForeignKey(Requester)
    questions = models.ManyToManyField(Question)
    
class Proposal(models.Model):
    application = models.ForeignKey(Application)
    
class Item(models.Model):
    proposal = models.ForeignKey(Proposal)
    name = models.CharField(max_length=64)
    amount = models.DecimalField(decimal_places=2)

class Grant(models.Model):
    funder = models.ForeignKey(Funder)
    item = models.ForeignKey(Item)
    amount = models.DecimalField(decimal_places=2)

class Answer(models.Model):
    question = models.ForeignKey(Question)
    content = models.CharField(max_length=64)
