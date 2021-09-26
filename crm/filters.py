from django_filters import rest_framework as filters

from .models import Client, Contract, Event


class ClientFilter(filters.FilterSet):
    last_name_contains = filters.CharFilter(
        field_name="last_name",
        lookup_expr='icontains'
    )

    first_name_contains = filters.CharFilter(
        field_name="first_name",
        lookup_expr='icontains'
    )

    email_contains = filters.CharFilter(
        field_name="email",
        lookup_expr='icontains'
    )

    company_contains = filters.DateFilter(
        field_name="company",
        lookup_expr='icontains'
    )

    class Meta:
        model = Client
        fields = [
            'last_name',
            'first_name',
            'sales_contact',
            'email',
            'phone',
            'mobile',
            'company',
            'date_created',
            'date_updated'
        ]


class ContractFilter(filters.FilterSet):
    class Meta:
        model = Contract
        fields = [
            'status',
            'sales_contact',
            'amount',
            'payment_due',
            'date_created',
            'date_updated'
        ]


class EventFilter(filters.FilterSet):
    notes_contains = filters.CharFilter(
        field_name="notes",
        lookup_expr='icontains'
    )

    class Meta:
        model = Event
        fields = [
            'support_contact',
            'attendees',
            'notes',
            'event_date',
            'date_created',
            'date_updated'
        ]
