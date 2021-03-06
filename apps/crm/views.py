from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets
from django_filters import rest_framework as filters

from .exceptions import NotFoundException, EventAlreadyExists
from .filters import ClientFilter, EventFilter, ContractFilter
from .models import Client, Contract, Event
from .serializers import ClientSerializer, ContractSerializer, EventSerializer, \
    ClientSerializerForManager
from .permissions import ClientAccess, ContractAccess, EventAccess, IsManager


class CRMBaseViewSet(viewsets.ModelViewSet):
    client = None
    contract = None

    def get_client(self):
        """
        Checks if the client_id url variable is corresponding to an existing client and
        returns this client if any.
        """
        client_id = self.kwargs['client_id']
        try:
            client = Client.objects.get(pk=client_id)
        except ObjectDoesNotExist:
            raise NotFoundException()
        return client

    def get_contract(self):
        """
        Checks if the contract_id url variable is corresponding to an existing contract and is
        associated with the correct client and returns this contract if everything is OK.
        """
        contract_id = self.kwargs['contract_id']
        try:
            contract = Contract.objects.get(pk=contract_id)
        except ObjectDoesNotExist:
            raise NotFoundException()
        if contract.client != self.client:
            raise NotFoundException()
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
            raise EventAlreadyExists()
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
