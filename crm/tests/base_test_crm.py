from django.contrib.auth.models import User
from django.core.management import call_command
from rest_framework.test import APITestCase


class CRMBaseTestCase(APITestCase):
    def setUp(self):
        call_command('loaddata', 'fixtures/tests_fixtures.json', verbosity=0)

        self.undefined_user = User.objects.get(username="undefined")

        self.salesman_with_client = User.objects.get(username="salesman_with_client")
        self.salesman_wo_client = User.objects.get(username="salesman_wo_client")

        self.support_with_event = User.objects.get(username="support_with_event")
        self.support_wo_event = User.objects.get(username="support_wo_event")


