from django.urls import reverse
from rest_framework import status

from .base_test_crm import CRMBaseTestCase
from crm.models import Event


class EventTestCase(CRMBaseTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.list_kwargs = {
            "client_id": 1,
            "contract_id": 1
        }

        cls.detail_kwargs = {
            "client_id": 1,
            "contract_id": 1,
            "pk": 1
        }

        cls.event_post_form = {
            "attendees": "1",
            "notes": "test_notes",
            "event_date": "2022-10-09 23:55"
        }

        cls.event_put_form = {
            "attendees": "99",
            "notes": "modified_notes",
            "event_date": "2024-10-09 23:55"
        }


class AnonTestCase(EventTestCase):
    def test_event_list_anon(self):
        response = self.client.get(reverse('events-list', kwargs=self.list_kwargs))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_event_retrieve_anon(self):
        response = self.client.get(reverse('events-detail', kwargs=self.detail_kwargs))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_event_post_anon(self):
        event = Event.objects.get(pk=1)
        event.delete()
        response = self.client.post(reverse('events-list', kwargs=self.list_kwargs),
                                    data=self.event_post_form)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_event_put_anon(self):
        response = self.client.put(reverse('events-detail', kwargs=self.detail_kwargs),
                                   data=self.event_put_form)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_event_delete_anon(self):
        response = self.client.get(reverse('events-detail', kwargs=self.detail_kwargs))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UndefindedUserTestCase(EventTestCase):
    def setUp(self):
        self.client.force_authenticate(user=self.undefined_user)

    def test_event_list_undefined(self):
        response = self.client.get(reverse('events-list', kwargs=self.list_kwargs))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_event_retrieve_undefined_user(self):
        response = self.client.get(reverse('events-detail', kwargs=self.detail_kwargs))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_event_post_undefined_user(self):
        event = Event.objects.get(pk=1)
        event.delete()
        response = self.client.post(reverse('events-list', kwargs=self.list_kwargs),
                                    data=self.event_post_form)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_event_put_undefined_user(self):
        response = self.client.put(reverse('events-detail', kwargs=self.detail_kwargs),
                                   data=self.event_put_form)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_event_delete_undefined_user(self):
        response = self.client.delete(reverse('events-detail', kwargs=self.detail_kwargs))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SalesmanWithClientTestCase(EventTestCase):
    def setUp(self):
        self.client.force_authenticate(user=self.salesman_with_client)

    def test_event_list_salesman_with_client(self):
        response = self.client.get(reverse('events-list', kwargs=self.list_kwargs))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_retrieve_salesman_with_client(self):
        response = self.client.get(reverse('events-detail', kwargs=self.detail_kwargs))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_post_salesman_with_client(self):
        event = Event.objects.get(pk=1)
        event.delete()
        response = self.client.post(reverse('events-list', kwargs=self.list_kwargs),
                                    data=self.event_post_form)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_event_put_salesman_with_client(self):
        response = self.client.put(reverse('events-detail', kwargs=self.detail_kwargs),
                                   data=self.event_put_form)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_event_delete_salesman_with_client(self):
        response = self.client.delete(reverse('events-detail', kwargs=self.detail_kwargs))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SalesmanWithoutClientTestCase(EventTestCase):
    def setUp(self):
        self.client.force_authenticate(user=self.salesman_wo_client)

    def test_event_list_salesman_wo_client(self):
        response = self.client.get(reverse('events-list', kwargs=self.list_kwargs))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_retrieve_salesman_wo_client(self):
        self.client.force_authenticate(user=self.salesman_wo_client)
        response = self.client.get(reverse('events-detail', kwargs=self.detail_kwargs))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_post_salesman_wo_client(self):
        event = Event.objects.get(pk=1)
        event.delete()
        response = self.client.post(reverse('events-list', kwargs=self.list_kwargs),
                                    data=self.event_post_form)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_event_put_salesman_wo_client(self):
        self.client.force_authenticate(user=self.salesman_wo_client)
        response = self.client.put(reverse('events-detail', kwargs=self.detail_kwargs),
                                   data=self.event_put_form)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_event_delete_salesman_wo_client(self):
        response = self.client.delete(reverse('events-detail', kwargs=self.detail_kwargs))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SupportWithEventTestCase(EventTestCase):
    def setUp(self):
        self.client.force_authenticate(user=self.support_with_event)

    def test_event_list_support_with_event(self):
        response = self.client.get(reverse('events-list', kwargs=self.list_kwargs))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_retrieve_support_with_event(self):
        response = self.client.get(reverse('events-detail', kwargs=self.detail_kwargs))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_post_support_with_event(self):
        event = Event.objects.get(pk=1)
        event.delete()
        response = self.client.post(reverse('events-list', kwargs=self.list_kwargs),
                                    data=self.event_post_form)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_event_put_support_with_event(self):
        response = self.client.put(reverse('events-detail', kwargs=self.detail_kwargs),
                                   data=self.event_put_form)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_delete_support_with_event(self):
        response = self.client.delete(reverse('events-detail', kwargs=self.detail_kwargs))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SupportWithoutEventTestCase(EventTestCase):
    def setUp(self):
        self.client.force_authenticate(user=self.support_wo_event)

    def test_event_list_support_wo_event(self):
        response = self.client.get(reverse('events-list', kwargs=self.list_kwargs))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_retrieve_support_wo_event(self):
        response = self.client.get(reverse('events-detail', kwargs=self.detail_kwargs))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_post_support_wo_event(self):
        event = Event.objects.get(pk=1)
        event.delete()
        response = self.client.post(reverse('events-list', kwargs=self.list_kwargs),
                                    data=self.event_post_form)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_event_put_support_wo_event(self):
        response = self.client.put(reverse('events-detail', kwargs=self.detail_kwargs),
                                   data=self.event_put_form)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_event_delete_support_wo_event(self):
        response = self.client.delete(reverse('events-detail', kwargs=self.detail_kwargs))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ManagerTestCase(EventTestCase):
    def setUp(self):
        self.client.force_authenticate(user=self.manager)

    def test_event_list_manager(self):
        response = self.client.get(reverse('events-list', kwargs=self.list_kwargs))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_retrieve_manager(self):
        response = self.client.get(reverse('events-detail', kwargs=self.detail_kwargs))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_post_manager(self):
        event = Event.objects.get(pk=1)
        event.delete()
        response = self.client.post(reverse('events-list', kwargs=self.list_kwargs),
                                    data=self.event_post_form)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_event_put_manager(self):
        response = self.client.put(reverse('events-detail', kwargs=self.detail_kwargs),
                                   data=self.event_put_form)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_delete_manager(self):
        response = self.client.delete(reverse('events-detail', kwargs=self.detail_kwargs))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
