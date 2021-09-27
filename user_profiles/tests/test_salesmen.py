from django.urls import reverse
from rest_framework import status

from .base_test_profiles import CRMBaseTestCase


class SalesmenTestCase(CRMBaseTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.salesman_form = {
            'user': 1,
        }


class AnonProfileTestCase(SalesmenTestCase):
    def test_users_list_anon(self):
        response = self.client.get(reverse('salesmen-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_retrieve_anon(self):
        response = self.client.get(reverse('salesmen-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_post_anon(self):
        response = self.client.post(reverse('salesmen-list'), data=self.salesman_form)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_delete_anon(self):
        response = self.client.delete(reverse('salesmen-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UndefinedProfileTestCase(SalesmenTestCase):
    def setUp(self):
        self.client.force_authenticate(user=self.undefined_user)

    def test_users_list_undefined(self):
        response = self.client.get(reverse('salesmen-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_users_retrieve_undefined(self):
        response = self.client.get(reverse('salesmen-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_users_post_undefined(self):
        response = self.client.post(reverse('salesmen-list'), data=self.salesman_form)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_users_delete_undefined(self):
        response = self.client.delete(reverse('salesmen-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SalesmanProfileTestCase(SalesmenTestCase):
    def setUp(self):
        self.client.force_authenticate(user=self.salesman_with_client)

    def test_users_list_salesman(self):
        response = self.client.get(reverse('salesmen-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_users_retrieve_salesman(self):
        response = self.client.get(reverse('salesmen-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_users_post_salesman(self):
        response = self.client.post(reverse('salesmen-list'), data=self.salesman_form)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_users_delete_salesman(self):
        response = self.client.delete(reverse('salesmen-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SupportProfileTestCase(SalesmenTestCase):
    def setUp(self):
        self.client.force_authenticate(user=self.support_with_event)

    def test_users_list_support(self):
        response = self.client.get(reverse('salesmen-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_users_retrieve_support(self):
        response = self.client.get(reverse('salesmen-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_users_post_support(self):
        response = self.client.post(reverse('salesmen-list'), data=self.salesman_form)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_users_delete_support(self):
        response = self.client.delete(reverse('salesmen-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ManagerProfileTestCase(SalesmenTestCase):
    def setUp(self):
        self.client.force_authenticate(user=self.manager)

    def test_users_list_manager(self):
        response = self.client.get(reverse('salesmen-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_retrieve_manager(self):
        response = self.client.get(reverse('salesmen-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_post_manager(self):
        response = self.client.post(reverse('salesmen-list'), data=self.salesman_form)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_users_delete_manager(self):
        response = self.client.delete(reverse('salesmen-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
