import datetime
import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from app.models import *

from sandbox_config import URL_ROOT, TEST_EMAIL


QUESTIONS = [
    {
        'q': ("Is your event primarily a speaker event (i.e., "
            "over 50% speaking)?"),
        'ys': ['connaissance'],
        'ns': ['tchange']
        },
    {
        'q': ("Is your event primarily a performance event (i.e., over 50% "
            "performance, not including speaking)?"),
        'ys': [],
        'ns': []
        },
    {
        'q': "Is alcohol served at your event?",
        'ys': [],
        'ns': ['spectrum', 'connaissance', 'fullyplanned', 'icf', 'faithfund',
            'tchange', 'uacontingency']
        },
    {
        'q': "Is your event a fundraiser for your group?", #TODO: Differentiate?
        'ys': [],
        'ns': ['spectrum', 'connaissance', 'fullyplanned', 'icf', 'tchange']
        },
    {
        'q': "Is your event a closed event?",
        'ys': [],
        'ns': ['spectrum', 'icf', 'faithfund', 'tchange']
        },
    {
        'q': ("Does your event involve multiple student organizations and "
            "undergraduate communities?"),
        'ys': ['icf', 'tchange'],
        'ns': []
        },
    {
        'q': ("Does this event does transport students via a private "
            "transport service?"),
        'ys': [],
        'ns': ['tchange']
        },
    {
        'q': "Are all your groups University-recognized?",
        'ys': ['icf'],
        'ns': []
        },
]

COMMON_QS = [
    ("What are the goals and mission of your event and how do the "
     "relate to the missions of all groups involved?"),
    ("Describe in detail the nature of your event and the timeline for "
     "its completion."),
    ("Please list three past events held by the collaborating "
     "organizations and describe their outcomes."),
    ("How do you plan to publicize this event?"),
    ]


REQUESTERS = [
    'philo',
    'testrequester1',
    'testrequester2',
    'testrequester3',
    ]

FUNDERS = [
    {
        'name': 'SPEC-TRUM',
        'un': 'spectrum',
        'desc': 'Host events serving multitude of minority interests on campus.',
        'qs': []
        },

    {
        'name': 'SPEC Connaissance',
        'un': 'connaissance',
        'desc': 'Bring awesome speakers.',
        'qs': []
        },

    {
        'name': 'SPEC Fully Planned',
        'un': 'fullyplanned',
        'desc': ('Fund events that are ready to go but need financial '
               'assistance to be viable.'),
        'qs': []
        },

    {
        'name': 'Intercultural Fund',
        'un': 'icf',
        'desc': ('Fund events where at least one group sponsoring event '
               'must be 5B.'),
        'qs': [
            ('Please list which of the 5B groups are involved in your '
             'event (i.e., APSC, Lambda, PCUW, UMOJA, and/or UMC).'),
            ("How does your event fulfill the mission of the "
             "Intercultural Fund?"),
            
            ]
        },

    {
        'name': 'Faith Fund',
        'un': 'faithfund',
        'desc': ('Promote and support faith-based events that are '
               'educational in nature and not exclusive'),
        'qs': []
        },

    {
        'name': 'T-Change',
        'un': 'tchange',
        'desc': ('Fund collaborative events that promote interaction among '
               'disparate audiences.'),
        'qs': [
            ("The Vice-Provost of University Life (VPUL) charges "
             "Tangible Change with funding unique events that bring "
             "together disparate and/or diverse undergraduate "
             "communities. Explain how your event meets this criterion. "
             "(Up to 300 words.)"),
            ("Please detail the nature of collaboration between your "
             "event's collaborating groups. (Up to 200 words.)"),
            ("Please list the past 3 major events hosted by your "
             "event's collaborating organizations.")
            ]
        },

    {
        'name': 'UA Contingency',
        'un': 'uacontingency',
        'desc': ('Fund events that need funding and have exhausted their other '
               'alternatives.'),
        'qs': []
        }
    ]


def add_funder(name, un, desc, qs):
    """Add a funder and their attendant questions."""
    # User and CFAUser
    user = User.objects.create_user(
        username=un,
        password=un,
        email=TEST_EMAIL)
    user.first_name = name[:30]
    profile = user.get_profile()
    profile.user_type = 'F'
    profile.mission_statement = desc
    profile.osa_email = TEST_EMAIL
    profile.save()

    # Questions
    for q in qs:
        FreeResponseQuestion.objects.create(funder=profile, question=q)


def add_requester(un):
    """Import a dummy requester."""
    User.objects.create_user(username=un, email=TEST_EMAIL, password=un)


def import_users():
    """Import all the funders described above."""
    CFAUser.objects.all().delete()
    User.objects.filter(is_staff=False).delete()
    FreeResponseQuestion.objects.all().delete()

    # Import funders
    for funder in FUNDERS:
        add_funder(**funder)

    # Import requesters
    for requester in REQUESTERS:
        add_requester(requester)


def import_questions():
    """Import the common and eligibility questions. Should be run after
    import_funders."""
    EligibilityQuestion.objects.all().delete()
    FunderConstraint.objects.all().delete()
    for question in QUESTIONS:
        q = EligibilityQuestion.objects.create(question=question['q'])
        for y in question['ys']:
            FunderConstraint.objects.create(
                funder=User.objects.get(username=y).cfauser,
                question=q, answer='Y')
        for n in question['ns']:
            FunderConstraint.objects.create(
                funder=User.objects.get(username=n).cfauser,
                question=q, answer='N')

    CommonFreeResponseQuestion.objects.all().delete()
    for common_q in COMMON_QS:
        CommonFreeResponseQuestion.objects.create(question=common_q)
        

def import_sites():
  site = Site.objects.get_current()
  site.domain = "www.pennapps.com%s/" % URL_ROOT
  site.name = "The Common Funding App"
  site.save()


def import_all():
    import_users()
    import_questions()
    import_sites()
    return 0

if __name__ == '__main__':
    sys.exit(import_all())
