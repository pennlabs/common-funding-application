import datetime
import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from app.models import *

from sandbox_config import URL_ROOT


QUESTIONS = [
    "Is your event primarily a speaker event (i.e. over 50% speaking)?",
    "If your event features a speaker or performance, does it include any kind of interactive components?",
    "Is alcohol served at your event?",
    "Is your event a closed event?",
    "Does your event serve minority interests on campus?",
]


def import_questions():
    EligibilityQuestion.objects.all().delete()
    for question in QUESTIONS:
        EligibilityQuestion.objects.create(question=question)


def import_users():
    CFAUser.objects.all().delete()
    User.objects.filter(is_staff=False).delete()
    User.objects.create_user(username="testrequester1",
        email="testrequester1@test.com",
        password="testrequester1")
    User.objects.create_user(username="testrequester2",
        email="testrequester2@test.com",
        password="testrequester2")
    funder1 = User.objects.create_user(username="testfunder1",
        email="testfunder1@test.com",
        password="testfunder1")
    profile1 = funder1.get_profile()
    profile1.user_type = 'F'
    profile1.save()
    funder2 = User.objects.create_user(username="testfunder2",
        email="topwolfed@gmail.com",
        password="testfunder2")
    profile2 = funder2.get_profile()
    profile2.user_type = 'F'
    profile2.save()


COMMON_FREE_RESPONSE_QUESTIONS = (
    "Describe your event.",
    "What are the goals of your event and how do they relate to the missions of all groups involved?",
    "How do you plan to publicize this event?",
    "Please detail the nature of collaboration between your event's collaborating groups.",
    "Please list three past events held by the collaborating organizations."
    )


def import_free_response():
    CommonFreeResponseQuestion.objects.all().delete()
    for question in COMMON_FREE_RESPONSE_QUESTIONS:
      cfrq = CommonFreeResponseQuestion.objects.create(question=question)


def import_constraints():
    FunderConstraint.objects.all().delete()
    FunderConstraint.objects.create(funder=User.objects.get(username="testfunder1").cfauser,
                                    question=EligibilityQuestion.objects.get(question=QUESTIONS[2]),
                                    answer='N')
    FunderConstraint.objects.create(funder=User.objects.get(username="testfunder2").cfauser,
                                    question=EligibilityQuestion.objects.get(question=QUESTIONS[2]),
                                    answer='N')
    FunderConstraint.objects.create(funder=User.objects.get(username="testfunder2").cfauser,
                                    question=EligibilityQuestion.objects.get(question=QUESTIONS[4]),
                                    answer='Y')



def import_events():
    Event.objects.all().delete()
    Event.objects.create(name="testrequester1's First Event",
                         date=datetime.date(year=2012,
                                            month=4,
                                            day=1),
                         time=datetime.time(hour=12),
                         location='Huntsman',
                         anticipated_attendance=0,
                         admission_fee='0',
                         requester=CFAUser.objects.get(user=User.objects.get(username="testrequester1")))
    Event.objects.create(name="testrequester1's Second Event",
                         date=datetime.date(year=2012,
                                            month=4,
                                            day=2),
                         time=datetime.time(hour=13),
                         location='Moore 100',
                         anticipated_attendance=50,
                         admission_fee='69.69',
                         requester=CFAUser.objects.get(user=User.objects.get(username="testrequester1")))
    Event.objects.create(name="testrequester2's First Event",
                         date=datetime.date(year=2012,
                                            month=5,
                                            day=1),
                         time=datetime.time(hour=14),
                         location='DRLB',
                         anticipated_attendance=30,
                         admission_fee='10',
                         requester=CFAUser.objects.get(user=User.objects.get(username="testrequester2")))
    Event.objects.create(name="testrequester2's Second Event",
                         date=datetime.date(year=2012,
                                            month=5,
                                            day=2),
                         time=datetime.time(hour=20),
                         location='Rodin',
                         anticipated_attendance=10,
                         admission_fee='8',
                         requester=CFAUser.objects.get(user=User.objects.get(username="testrequester2")))

def import_sites():
  site = Site.objects.get_current()
  site.domain = "www.pennapps.com%s/" % URL_ROOT
  site.name = "The Common Funding App"
  site.save()

def import_all():
    import_questions()
    import_users()
    import_free_response()
    import_constraints()
    import_events()
    import_sites()
    return 0

if __name__ == '__main__':
    sys.exit(import_all())
