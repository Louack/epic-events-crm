from django.urls import reverse
from rest_framework import status

from .base_test_crm import CRMBaseTestCase


class ContractTestCase(CRMBaseTestCase):
    def setUp(self):
        super().setUp()

        self.list_kwargs = {"client_id": 1}
        self.detail_kwargs = {"client_id": 1,
                              "pk": 1}

        self.contract_post_form = {
            "status": "True",
            "amount": 100,
            "payment_due": "2022-10-09 23:55"
            }

        self.contract_put_form = {
            "status": "False",
            "amount": 999,
            "payment_due": "2024-10-09 23:55"
        }


class AnonTestCase(ContractTestCase):
    def test_contract_list_anon(self):
        response = self.client.get(reverse('contracts-list', kwargs=self.list_kwargs))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_contract_retrieve_anon(self):
        response = self.client.get(reverse('contracts-detail', kwargs=self.detail_kwargs))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_contract_post_anon(self):
        response = self.client.post(reverse('contracts-list', kwargs=self.list_kwargs),
                                    data=self.contract_post_form)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_contract_put_anon(self):
        response = self.client.put(reverse('contracts-detail', kwargs=self.detail_kwargs),
                                   data=self.contract_put_form)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_contract_delete_anon(self):
        response = self.client.get(reverse('contracts-detail', kwargs=self.detail_kwargs))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UndefindedUserTestCase(ContractTestCase):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.undefined_user)

    def test_contract_list_undefined(self):
        response = self.client.get(reverse('contracts-list', kwargs=self.list_kwargs))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_contract_retrieve_undefined_user(self):
        response = self.client.get(reverse('contracts-detail', kwargs=self.detail_kwargs))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_contract_post_undefined_user(self):
        response = self.client.post(reverse('contracts-list', kwargs=self.list_kwargs),
                                    data=self.contract_post_form)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_contract_put_undefined_user(self):
        response = self.client.put(reverse('contracts-detail', kwargs=self.detail_kwargs),
                                   data=self.contract_put_form)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_contract_delete_undefined_user(self):
        response = self.client.delete(reverse('contracts-detail', kwargs=self.detail_kwargs))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SalesmanWithClientTestCase(ContractTestCase):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.salesman_with_client)

    def test_contract_list_salesman_with_client(self):
        response = self.client.get(reverse('contracts-list', kwargs=self.list_kwargs))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_contract_retrieve_salesman_with_client(self):
        response = self.client.get(reverse('contracts-detail', kwargs=self.detail_kwargs))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_contract_post_salesman_with_client(self):
        response = self.client.post(reverse('contracts-list', kwargs=self.list_kwargs),
                                    data=self.contract_post_form)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_contract_put_salesman_with_client(self):
        response = self.client.put(reverse('contracts-detail', kwargs=self.detail_kwargs),
                                   data=self.contract_put_form)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_contract_delete_salesman_with_client(self):
        response = self.client.delete(reverse('contracts-detail', kwargs=self.detail_kwargs))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SalesmanWithoutClientTestCase(ContractTestCase):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.salesman_wo_client)

    def test_contract_list_salesman_wo_client(self):
        response = self.client.get(reverse('contracts-list', kwargs=self.list_kwargs))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_contract_retrieve_salesman_wo_client(self):
        self.client.force_authenticate(user=self.salesman_wo_client)
        response = self.client.get(reverse('contracts-detail', kwargs=self.detail_kwargs))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_contract_post_salesman_wo_client(self):
        response = self.client.post(reverse('contracts-list', kwargs=self.list_kwargs),
                                    data=self.contract_post_form)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_contract_put_salesman_wo_client(self):
        self.client.force_authenticate(user=self.salesman_wo_client)
        response = self.client.put(reverse('contracts-detail', kwargs=self.detail_kwargs),
                                   data=self.contract_put_form)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_contract_delete_salesman_wo_client(self):
        response = self.client.delete(reverse('contracts-detail', kwargs=self.detail_kwargs))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SupportTestCase(ContractTestCase):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.support_with_event)

    def test_contract_list_support(self):
        response = self.client.get(reverse('contracts-list', kwargs=self.list_kwargs))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_contract_retrieve_support(self):
        response = self.client.get(reverse('contracts-detail', kwargs=self.detail_kwargs))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_contract_post_support(self):
        response = self.client.post(reverse('contracts-list', kwargs=self.list_kwargs),
                                    data=self.contract_post_form)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_contract_put_support(self):
        response = self.client.put(reverse('contracts-detail', kwargs=self.detail_kwargs),
                                   data=self.contract_put_form)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_contract_delete_support(self):
        response = self.client.delete(reverse('contracts-detail', kwargs=self.detail_kwargs))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
