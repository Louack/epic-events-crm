from django.urls import reverse
from rest_framework import status

from .base_test_crm import CRMBaseTestCase


class ClientTestCase(CRMBaseTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client_post_form = {
            "first_name": "test",
            "last_name": "test",
            "email": "test@email.com",
            "phone": "123456789",
            "mobile": "123456789",
            "company": "test_company",
            "sales_contact": 1
        }

        cls.client_put_form = {
            "first_name": "modified",
            "last_name": "modified",
            "email": "email@test.com",
            "phone": "987654321",
            "mobile": "987654321",
            "company": "company_test"
        }


class AnonTestCase(ClientTestCase):
    def test_client_list_anon(self):
        response = self.client.get(reverse('clients-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_client_retrieve_anon(self):
        response = self.client.get(reverse('clients-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_client_post_anon(self):
        response = self.client.post(reverse('clients-list'),
                                    data=self.client_post_form)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_client_put_anon(self):
        response = self.client.put(reverse('clients-detail', kwargs={'pk': 1}),
                                   data=self.client_put_form)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_client_delete_anon(self):
        response = self.client.get(reverse('clients-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UndefindedUserTestCase(ClientTestCase):
    def setUp(self):
        self.client.force_authenticate(user=self.undefined_user)

    def test_client_list_undefined(self):
        response = self.client.get(reverse('clients-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_client_retrieve_undefined_user(self):
        response = self.client.get(reverse('clients-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_client_post_undefined_user(self):
        response = self.client.post(reverse('clients-list'),
                                    data=self.client_post_form)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_client_put_undefined_user(self):
        response = self.client.put(reverse('clients-detail', kwargs={'pk': 1}),
                                   data=self.client_put_form)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_client_delete_undefined_user(self):
        response = self.client.delete(reverse('clients-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SalesmanWithClientTestCase(ClientTestCase):
    def setUp(self):
        self.client.force_authenticate(user=self.salesman_with_client)

    def test_client_list_salesman_with_client(self):
        response = self.client.get(reverse('clients-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_client_retrieve_salesman_with_client(self):
        response = self.client.get(reverse('clients-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_client_post_salesman_with_client(self):
        response = self.client.post(reverse('clients-list'),
                                    data=self.client_post_form)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_client_put_salesman_with_client(self):
        response = self.client.put(reverse('clients-detail', kwargs={'pk': 1}),
                                   data=self.client_put_form)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_client_delete_salesman_with_client(self):
        response = self.client.delete(reverse('clients-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SalesmanWithoutClientTestCase(ClientTestCase):
    def setUp(self):
        self.client.force_authenticate(user=self.salesman_wo_client)

    def test_client_list_salesman_wo_client(self):
        response = self.client.get(reverse('clients-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_client_retrieve_salesman_wo_client(self):
        self.client.force_authenticate(user=self.salesman_wo_client)
        response = self.client.get(reverse('clients-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_client_post_salesman_wo_client(self):
        response = self.client.post(reverse('clients-list'),
                                    data=self.client_post_form)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_client_put_salesman_wo_client(self):
        self.client.force_authenticate(user=self.salesman_wo_client)
        response = self.client.put(reverse('clients-detail', kwargs={'pk': 1}),
                                   data=self.client_put_form)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_client_delete_salesman_wo_client(self):
        response = self.client.delete(reverse('clients-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SupportTestCase(ClientTestCase):
    def setUp(self):
        self.client.force_authenticate(user=self.support_with_event)

    def test_client_list_support(self):
        response = self.client.get(reverse('clients-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_client_retrieve_support(self):
        response = self.client.get(reverse('clients-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_client_post_support(self):
        response = self.client.post(reverse('clients-list'),
                                    data=self.client_post_form)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_client_put_support(self):
        response = self.client.put(reverse('clients-detail', kwargs={'pk': 1}),
                                   data=self.client_put_form)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_client_delete_support(self):
        response = self.client.delete(reverse('clients-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ManagerTestCase(ClientTestCase):
    def setUp(self):
        self.client_post_form['sales_contact'] = 1
        self.client_put_form['sales_contact'] = 1
        self.client.force_authenticate(user=self.manager)

    def test_client_list_manager(self):
        response = self.client.get(reverse('clients-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_client_retrieve_manager(self):
        response = self.client.get(reverse('clients-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_client_post_manager(self):
        response = self.client.post(reverse('clients-list'),
                                    data=self.client_post_form)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_client_put_manager(self):
        response = self.client.put(reverse('clients-detail', kwargs={'pk': 1}),
                                   data=self.client_put_form)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_client_delete_manager(self):
        response = self.client.delete(reverse('clients-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
