from django.db import models

# Create your models here.
class Requester(models.Model):
    user = models.ForeignKey(models.User)

class Funder(models.Model):
    user = models.ForeignKey(models.User)

class Application(model.Model):
    requester = models.ForeignKey(Requester)
    questions = models.ManyToManyField(Question)
    
class Proposal(models.Model):
    application = models.ForeignKey(Application)
    
class Item(model.Model):
    proposal = models.ForeignKey(Proposal)
    name = models.CharField(max_length=64)
    amount = models.DecimalField(decimal_places=2)

class Grant(model.Model):
    funder = models.ForeignKey(Funder)
    item = models.ForeignKey(Item)
    amount = models.DecimalField(decimal_places=2)
    
class Question(model.Model):
    content = model.TextField()
    format = models.CharField(max_length=16)

class Answer(model.Model):
    question = model.ForeignKey(Question)
    content = models.CharField(max_length=64)
