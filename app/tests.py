from django.test import TestCase

from .models import CFAUser


class CFAUserTest(TestCase):
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
