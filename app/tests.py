from django.test import TestCase

from .models import CFAUser


class CFAUserTest(TestCase):
    def test_is_funder(self):
        cuser = CFAUser.objects.get(pk=1)
        self.assertTrue(cuser.is_funder)

    def test_is_requester(self):
        cuser = CFAUser.objects.get(pk=11)
        self.assertTrue(cuser.is_requester)
