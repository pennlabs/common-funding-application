import datetime

from django.contrib.auth.models import User

from app.models import *


QUESTIONS = [
    "Is your event primarily a speaker event (i.e. over 50% speaking)?",
    "If your event features a speaker or performance, does it include any kind of interactive components?",
    "Is alcohol served at your event?",
    "Is your event a closed event?",
    "Does your event serve minority interests on campus?",
]


def import_questions():
    Question.objects.all().delete()
    for question in QUESTIONS:
        Question.objects.create(question=question)


def import_users():
    CFAUser.objects.all().delete()
    User.objects.filter(is_staff=False).delete()
    CFAUser.objects.create(user=User.objects.create_user(username="testrequester1",
                                                         email="testrequester1@test.com",
                                                         password="testrequester1"), user_type='R')
    CFAUser.objects.create(user=User.objects.create_user(username="testrequester2",
                                                         email="testrequester2@test.com",
                                                         password="testrequester2"), user_type='R')
    CFAUser.objects.create(user=User.objects.create_user(username="testfunder1",
                                                         email="testfunder1@test.com",
                                                         password="testfunder1"), user_type='F')
    CFAUser.objects.create(user=User.objects.create_user(username="testfunder2",
                                                         email="testfunder2@test.com",
                                                         password="testfunder2"), user_type='F')


def import_constraints():
    FunderConstraint.objects.all().delete()
    FunderConstraint.objects.create(funder=User.objects.get(username="testfunder1").cfauser,
                                    question=Question.objects.get(question=QUESTIONS[2]),
                                    answer='N')
    FunderConstraint.objects.create(funder=User.objects.get(username="testfunder2").cfauser,
                                    question=Question.objects.get(question=QUESTIONS[2]),
                                    answer='N')
    FunderConstraint.objects.create(funder=User.objects.get(username="testfunder2").cfauser,
                                    question=Question.objects.get(question=QUESTIONS[4]),
                                    answer='Y')



def import_events():
    Event.objects.all().delete()
    Event.objects.create(name="testrequester1's First Event",
                         date=datetime.date(year=2012,
                                            month=4,
                                            day=1),
                         requester=CFAUser.objects.get(user=User.objects.get(username="testrequester1")))
    Event.objects.create(name="testrequester1's Second Event",
                         date=datetime.date(year=2012,
                                            month=4,
                                            day=2),
                         requester=CFAUser.objects.get(user=User.objects.get(username="testrequester1")))
    Event.objects.create(name="testrequester2's First Event",
                         date=datetime.date(year=2012,
                                            month=5,
                                            day=1),
                         requester=CFAUser.objects.get(user=User.objects.get(username="testrequester2")))
    Event.objects.create(name="testrequester2's Second Event",
                         date=datetime.date(year=2012,
                                            month=5,
                                            day=2),
                         requester=CFAUser.objects.get(user=User.objects.get(username="testrequester2")))
    

def import_all():
    import_questions()
    import_users()
    import_constraints()
    import_events()
