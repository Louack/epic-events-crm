from django.contrib.auth.models import User
from django.core.management import call_command
from rest_framework.test import APITestCase


class CRMBaseTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        call_command('loaddata', 'fixtures/tests_fixtures.json', verbosity=0)

        cls.undefined_user = User.objects.get(username="undefined")
        cls.salesman_with_client = User.objects.get(username="salesman_with_client")
        cls.salesman_wo_client = User.objects.get(username="salesman_wo_client")
        cls.support_with_event = User.objects.get(username="support_with_event")
        cls.support_wo_event = User.objects.get(username="support_wo_event")
        cls.manager = User.objects.get(username="manager")

    @classmethod
    def tearDownClass(cls):
        pass
