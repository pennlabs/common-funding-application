import json

from django.test import TestCase

from django.contrib.auth.models import User
from .models import CFAUser, Event


class CFAUserTest(TestCase):
    fixtures = ['cfausers.json']

    def test_is_funder(self):
        cuser = CFAUser.objects.get(pk=1)
        self.assertTrue(cuser.is_funder)

    def test_is_requester(self):
        cuser = CFAUser.objects.get(pk=11)
        self.assertTrue(cuser.is_requester)


class TestViews(TestCase):
    def test_index(self):
        """Test to see that index redirects to login page

        TODO: In the future, index page should be the login page
        """
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 302)

    def test_login_page(self):
        resp = self.client.get('/accounts/login/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('form' in resp.context)
        self.assertContains(resp, 'Login')


class TestLoginViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='philo',
                                             email='philo@upenn.edu',
                                             password='we<3literature')

    def test_index(self):
        self.client.login(username='philo', password='we<3literature')
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Current Applications')

    def test_index_not_logged_in(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 302)

    def test_logout(self):
        self.client.login(username='philo', password='we<3literature')
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.client.logout()
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 302)


class TestEvents(TestCase):
    fixtures = ['events.json']

    def setUp(self):
        self.user = User.objects.create_user(username='philo',
                                             email='philo@upenn.edu',
                                             password='we<3literature')
        self.client.login(username='philo', password='we<3literature')

    def test_index(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Current Applications')
        self.assertContains(resp, 'Penn Labs Team')
        self.assertContains(resp, 'SUBMITTED')

    def test_index_remove_event(self):
        Event.objects.get(pk=1).delete()
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Current Applications')
        self.assertContains(resp, "You do not have any current applications.")
        resp = self.client.get('/1/')
        self.assertEqual(resp.status_code, 404)

    def test_edit_event(self):
        resp = self.client.get('/1/edit/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Houston Hall')

    def test_edit_event_location(self):
        with open('app/fixtures/event_edit.json', 'r') as f:
            resp = self.client.post('/1/edit/', json.load(f))
        self.assertEqual(resp.status_code, 302)
        resp = self.client.get('/1/edit/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'First Round')

    def test_event_is_old(self):
        # Push event into the past, currently 2050-01-01
        event = Event.objects.get(pk=1)
        event.date = '2000-01-01'
        event.save()
        # Ensure event isn't on the current applications page
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Current Applications')
        self.assertContains(resp, "You do not have any current applications.")
        # Ensure event still exists
        resp = self.client.get('/1/')
        self.assertEqual(resp.status_code, 200)
        # Ensure event is on the old applications page
        resp = self.client.get('/old/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Past Applications')
        self.assertContains(resp, 'Test Event')
