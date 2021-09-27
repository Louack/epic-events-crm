from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets
from django_filters import rest_framework as filters
import logging

from .exceptions import NotFoundException, EventAlreadyExists
from .filters import ClientFilter, EventFilter, ContractFilter
from .models import Client, Contract, Event
from .serializers import ClientSerializer, ContractSerializer, EventSerializer, ClientSerializerForManager
from .permissions import ClientAccess, ContractAccess, EventAccess, IsManager

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('crm.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class CRMBaseViewSet(viewsets.ModelViewSet):
    client = None
    contract = None

    def get_client(self):
        client_id = self.kwargs['client_id']
        try:
            client = Client.objects.get(pk=client_id)
        except ObjectDoesNotExist:
            message = 'Not found'
            logger.error(message)
            raise NotFoundException(message)
        return client

    def get_contract(self):
        contract_id = self.kwargs['contract_id']
        try:
            contract = Contract.objects.get(pk=contract_id)
        except ObjectDoesNotExist:
            message = 'Not found'
            logger.error(message)
            raise NotFoundException(message)
        if contract.client != self.client:
            message = 'Not found'
            logger.error(message)
            raise NotFoundException(message)
        return contract


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    permission_classes = [IsManager | ClientAccess]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ClientFilter

    def get_serializer_class(self):
        if hasattr(self.request.user, 'manager'):
            return ClientSerializerForManager
        else:
            return ClientSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if hasattr(self.request.user, 'salesman'):
            context['salesman'] = self.request.user.salesman
        return context


class ContractViewSet(CRMBaseViewSet):
    serializer_class = ContractSerializer
    permission_classes = [IsManager | ContractAccess]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ContractFilter

    def get_queryset(self):
        queryset = Contract.objects.filter(client=self.client)
        return queryset

    def initial(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            self.client = self.get_client()
        super().initial(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['client'] = self.client
        context['salesman'] = self.client.sales_contact
        return context


class EventViewSet(CRMBaseViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsManager | EventAccess]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EventFilter

    def initial(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            self.client = self.get_client()
            self.contract = self.get_contract()
        super().initial(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        if hasattr(self.contract, 'event'):
            message = f'An event already exists for {self.contract}'
            logger.error(message)
            raise EventAlreadyExists(message)
        else:
            return super().create(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Event.objects.filter(event_status=self.contract)
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['client'] = self.client
        context['contract'] = self.contract
        return context

