# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv
import json
from unittest import skip

from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase

from .models import CFAUser, Event, Grant
from .templatetags import helpers


def create_funder():
    funder = User.objects.create_user(
        username="spec", email="spec@upenn.edu", password="we<3money$$$"
    )
    cfau = funder.profile
    cfau.user_type = "F"
    cfau.save()
    return funder


class CFAUserTest(TestCase):
    fixtures = ["cfausers.json"]

    def test_is_funder(self):
        cuser = CFAUser.objects.get(pk=1)
        self.assertTrue(cuser.is_funder)

    def test_is_requester(self):
        cuser = CFAUser.objects.get(pk=11)
        self.assertTrue(cuser.is_requester)


class TestViews(TestCase):
    def test_index(self):
        """Test to see that index is the login page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Login")

    def test_login_page(self):
        resp = self.client.get("/accounts/login/")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue("form" in resp.context)
        self.assertContains(resp, "Login")


class TestRegistrationViews(TestCase):
    def test_register_page(self):
        resp = self.client.get("/accounts/register/")
        self.assertEqual(resp.status_code, 200)

    def test_register(self):
        resp = self.client.post(
            "/accounts/register/",
            data={
                "username": "philo",
                "email": "philo@upenn.edu",
                "password1": "we<3literature",
                "password2": "we<3literature",
            },
            follow=True,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(User.objects.filter(username="philo").exists())
        self.assertEqual(len(mail.outbox), 1)

    def test_reset_password(self):
        User.objects.create_user(
            username="philo", email="philo@upenn.edu", password="we<3literature"
        )

        resp = self.client.post(
            "/accounts/password/reset/", data={"email": "philo@upenn.edu"}, follow=True
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)

    def test_reset_password_invalid(self):
        resp = self.client.post(
            "/accounts/password/reset/",
            data={"email": "nonexistent@example.com"},
            follow=True,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)


class TestLoginViews(TestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="philo", email="philo@upenn.edu", password="we<3literature"
        )

    def test_index(self):
        self.client.login(username="philo", password="we<3literature")
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Current Applications")
        self.assertContains(resp, "Welcome, philo!")

    def test_index_not_logged_in(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Login")

    def test_logout(self):
        self.client.login(username="philo", password="we<3literature")
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.client.logout()
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Login")


class TestEvents(TestCase):
    fixtures = ["events.json"]

    def setUp(self):
        super().setUp()
        self.client.login(username="philo", password="we<3literature")

    def test_index(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Current Applications")
        self.assertContains(resp, "Penn Labs Team")
        self.assertContains(resp, "SUBMITTED")

    def test_index_remove_event(self):
        Event.objects.get(pk=1).delete()
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Current Applications")
        self.assertContains(resp, "No applications.")
        resp = self.client.get("/1/")
        self.assertEqual(resp.status_code, 404)

    def test_create_event(self):
        resp = self.client.get("/new/")
        with open("app/fixtures/event_edit.json", "r") as f:
            resp = self.client.post("/new/", json.load(f))
        self.assertEqual(resp.status_code, 302)
        event_id = Event.objects.get(name="Test").id
        resp = self.client.get("/{}/".format(event_id))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "First Round")

    def test_create_duplicate_event(self):
        resp = self.client.get("/new/")
        for _ in range(2):
            with open("app/fixtures/event_edit.json", "r") as f:
                resp = self.client.post("/new/", json.load(f))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Event.objects.filter(name="Test").count(), 1)

    def test_create_event_utf8(self):
        unicode_string = "Téßt؟"
        with open("app/fixtures/event_edit.json", "r") as f:
            data = json.load(f)
            data["name"] = unicode_string
            resp = self.client.post("/new/", data)
        self.assertEqual(resp.status_code, 302)
        event_id = Event.objects.get(name=unicode_string).id
        resp = self.client.get("/{}/".format(event_id))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, unicode_string)

    def test_edit_event(self):
        resp = self.client.get("/1/edit/")
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Houston Hall")

    def test_edit_event_location(self):
        with open("app/fixtures/event_edit.json", "r") as f:
            resp = self.client.post("/1/edit/", json.load(f))
        self.assertEqual(resp.status_code, 302)
        resp = self.client.get("/1/edit/")
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "First Round")

    def test_event_is_old(self):
        # Push event into the past, currently 2050-01-01
        event = Event.objects.get(pk=1)
        event.date = "2000-01-01"
        event.save()
        # Ensure event is on applications page
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Current Applications")
        self.assertContains(resp, "Test Event")
        # Ensure event still exists
        resp = self.client.get("/1/")
        self.assertEqual(resp.status_code, 200)


class TestFunder(TestCase):
    fixtures = ["events.json"]

    def setUp(self):
        super().setUp()
        self.user = User.objects.get(username="philo")
        self.funder = create_funder()
        self.client.login(username="spec", password="we<3money$$$")
        self.event = Event.objects.get(pk=1)

    def test_funder_is_funder(self):
        self.assertTrue(self.funder.profile.is_funder)
        self.assertTrue(self.user.profile.is_requester)

    @skip("Currently all funders have access to all applications")
    def test_event_no_funder_no_access(self):
        resp = self.client.get("/1/")
        self.assertEqual(resp.status_code, 302)

    def test_event_has_funder_has_access(self):
        self.event.applied_funders.add(self.funder.profile)
        resp = self.client.get("/1/")
        self.assertEqual(resp.status_code, 200)


class TestShare(TestCase):
    fixtures = ["events.json"]
    key = "a96055ddf995cce98469884fa202d3c40032e039"

    def setUp(self):
        super().setUp()
        self.event = Event.objects.get(pk=1)

    def test_event_secret_key(self):
        self.assertEqual(self.event.secret_key, TestShare.key)

    def test_event_share_link_no_access(self):
        resp = self.client.get("/1/")
        self.assertEqual(resp.status_code, 302)

    def test_event_access_with_login(self):
        self.client.login(username="philo", password="we<3literature")
        resp = self.client.get("/1/")
        self.assertEqual(resp.status_code, 200)

    def test_event_access_with_key(self):
        resp = self.client.get("/1/?key=" + TestShare.key)
        self.assertEqual(resp.status_code, 200)


class TestEmail(TestCase):
    fixtures = ["events.json"]

    def test_notify_requester(self):
        event = Event.objects.get(pk=1)
        event.notify_requester_for_followups()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Followup Questions for Test Event")


class TestEmailFunders(TestCase):
    fixtures = ["events.json"]

    def setUp(self):
        super().setUp()
        self.funder = create_funder()
        self.event = Event.objects.get(pk=1)
        self.event.applied_funders.add(self.funder.profile)

    def test_notify_funders(self):
        self.event.notify_funders()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject, "[Test Event] Event Application Changed"
        )


class TestItemGrant(TestCase):
    fixtures = ["events.json"]

    @staticmethod
    def create_item(event):
        return event.item_set.create(
            name="Free Software",
            quantity=10,
            price_per_unit=100,
            funding_already_received=0,
            category="H",
            revenue=0,
        )

    def setUp(self):
        super().setUp()
        self.funder = create_funder()
        self.event = Event.objects.get(pk=1)

    def test_total_amounts_not_funded(self):
        TestItemGrant.create_item(self.event)
        self.assertEqual(self.event.amounts, {})
        self.assertEqual(self.event.total_funds_granted, 0)

    def test_create_grant(self):
        item = TestItemGrant.create_item(self.event)
        grant = Grant.objects.create(funder=self.funder.profile, item=item, amount=50)
        grant.save()
        item.grant_set.add(grant)
        item.save()
        self.assertEqual(self.event.total_funds_granted, 50)


class TestHelpers(TestCase):
    fixtures = ["events.json"]

    def setUp(self):
        super().setUp()
        self.funder = create_funder()
        self.event = Event.objects.get(pk=1)
        self.item = TestItemGrant.create_item(self.event)
        grant = Grant.objects.create(
            funder=self.funder.profile, item=self.item, amount=50
        )
        grant.save()
        self.item.grant_set.add(grant)
        self.item.save()

    def test_funders_grant_data_to_item_no_grant(self):
        self.item.grant_set.all().delete()
        self.item.save()
        item_tuple = helpers.funders_grant_data_to_item(self.item, self.funder.id)
        self.assertEqual((None, self.item.id), item_tuple)

    def test_funders_grant_data_to_item(self):
        self.assertEqual(self.item.grant_set.count(), 1)

        item_tuple = helpers.funders_grant_data_to_item(
            self.item, self.funder.profile.id
        )
        self.assertEqual((50, self.item.id), item_tuple)

    def test_funder_item_data(self):
        self.assertEqual(self.item.grant_set.count(), 1)

        result = helpers.funder_item_data(self.item, [self.funder.profile])
        # funder data - funder id, amount = 50, grant id = 1
        expected = (self.item, [(self.funder.profile.id, 50, 1)])
        self.assertEqual(expected, result)

    def test_get_or_none_exists(self):
        self.assertEqual(self.event, helpers.get_or_none(Event, pk=1))

    def test_get_or_none_does_not_exist(self):
        self.assertEqual(None, helpers.get_or_none(Event, pk=2))


class HealthTestCase(TestCase):
    def test_health(self):
        resp = self.client.get("/health/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"message": "OK"})


class TestExportRequests(TestCase):
    def setUp(self):
        super().setUp()
        self.admin_user = User.objects.create_user(
            username="admin",
            email="admin@upenn.edu",
            password="adminpassword",
            is_staff=True,
        )
        self.requester = User.objects.create_user(
            username="requester",
            email="requester@upenn.edu",
            password="requesterpassword",
        )
        self.requester_profile = self.requester.profile
        self.requester_profile.user_type = "R"
        self.requester_profile.save()
        self.funder = create_funder()

        self.event1 = Event.objects.create(
            name="Test Event 1",
            date="2023-01-01",
            time="15:30:00",
            location="Houston Hall",
            requester=self.requester_profile,
            contact_name="Test Contact",
            contact_email="contact@upenn.edu",
            contact_phone="123-456-7890",
            anticipated_attendance=100,
            advisor_email="advisor@upenn.edu",
            advisor_phone="098-765-4321",
            organizations="Test Organization",
            funding_already_received=50.00,
            status="B",
        )
        self.event1.applied_funders.add(self.funder.profile)

        self.event2 = Event.objects.create(
            name="Test Event 2",
            date="2023-02-01",
            time="16:30:00",
            location="College Hall",
            requester=self.requester_profile,
            contact_name="Test Contact 2",
            contact_email="contact2@upenn.edu",
            contact_phone="123-456-7891",
            anticipated_attendance=200,
            advisor_email="advisor2@upenn.edu",
            advisor_phone="098-765-4322",
            organizations="Test Organization 2",
            funding_already_received=100.00,
            status="F",
        )
        self.event2.applied_funders.add(self.funder.profile)

        self.event3 = Event.objects.create(
            name="Test Event 3",
            date="2023-03-01",
            time="17:30:00",
            location="Van Pelt Library",
            requester=self.requester_profile,
            contact_name="Test Contact 3",
            contact_email="contact3@upenn.edu",
            contact_phone="123-456-7892",
            anticipated_attendance=300,
            advisor_email="advisor3@upenn.edu",
            advisor_phone="098-765-4323",
            organizations="Test Organization 3",
            funding_already_received=150.00,
            status="S",
        )

        self.item1 = self.event1.item_set.create(
            name="Item 1",
            quantity=10,
            price_per_unit=20.00,
            funding_already_received=0.00,
            category="H",
            revenue=False,
        )
        self.item2 = self.event1.item_set.create(
            name="Item 2",
            quantity=5,
            price_per_unit=30.00,
            funding_already_received=25.00,
            category="F",
            revenue=False,
        )
        self.item3 = self.event2.item_set.create(
            name="Item 3",
            quantity=15,
            price_per_unit=40.00,
            funding_already_received=50.00,
            category="E",
            revenue=False,
        )
        self.item4 = self.event2.item_set.create(
            name="Item 4 (Revenue)",
            quantity=20,
            price_per_unit=10.00,
            funding_already_received=0.00,
            category="O",
            revenue=True,
        )

        self.grant1 = Grant.objects.create(
            funder=self.funder.profile, item=self.item1, amount=100.00
        )
        self.grant2 = Grant.objects.create(
            funder=self.funder.profile, item=self.item3, amount=200.00
        )

    def test_export_requests_access(self):
        self.client.login(username="requester", password="requesterpassword")
        self.assertEqual(self.client.get("/export-requests/").status_code, 302)

        self.client.login(username="admin", password="adminpassword")
        resp = self.client.get("/export-requests/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp["Content-Type"], "text/csv")
        self.assertEqual(
            resp["Content-Disposition"], 'attachment; filename="funding_requests.csv"'
        )

    def test_export_requests_content(self):
        self.client.login(username="admin", password="adminpassword")
        resp = self.client.get("/export-requests/")
        content = resp.content.decode("utf-8")
        rows = list(csv.reader(content.strip().split("\n")))

        self.assertEqual(len(rows[0]), 25)
        self.assertEqual(rows[0][0], "Event ID")
        self.assertEqual(len(rows), 3)

        # Only submitted events should be included (not saved ones)
        event_names = [row[1] for row in rows[1:]]
        self.assertIn(
            "Test Event 2", event_names
        )  # sort in descending order of created_at
        self.assertIn("Test Event 1", event_names)
        self.assertNotIn("Test Event 3", event_names)

        event_row = rows[2]  # grab row for test event 1
        self.assertEqual(event_row[1], "Test Event 1")
        self.assertEqual(event_row[4], "Houston Hall")
        self.assertEqual(event_row[5], str(self.requester_profile))
        self.assertEqual(event_row[6], "requester@upenn.edu")
        self.assertEqual(event_row[14], "50.00")
        self.assertEqual(event_row[15], "SUBMITTED")

        self.assertEqual(float(event_row[18]), 75.00)
        self.assertEqual(float(event_row[19]), 100.00)
        self.assertEqual(float(event_row[20]), 175.00)
        self.assertEqual(float(event_row[21]), 350.00)
        self.assertEqual(float(event_row[22]), 0.00)
        self.assertEqual(float(event_row[23]), 175.00)
        self.assertIn(str(self.funder.profile), event_row[24])
