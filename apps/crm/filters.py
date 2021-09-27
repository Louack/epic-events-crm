from django_filters import rest_framework as filters

from .models import Client, Contract, Event


class ClientFilter(filters.FilterSet):

    min_date_created = filters.DateFilter(
        field_name="date_created",
        lookup_expr='gte')

    max_date_created = filters.DateFilter(
        field_name="date_created",
        lookup_expr='lte')

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

    company_contains = filters.CharFilter(
        field_name="company",
        lookup_expr='icontains'
    )

    sort_by = filters.CharFilter(
        method='filter_sort_by',
    )

    def filter_sort_by(self, queryset, name, value):
        values = value.lower().split(',')
        return queryset.order_by(*values)

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
            'date_updated',
            'min_date_created',
            'max_date_created',
            'sort_by'
        ]


class ContractFilter(filters.FilterSet):
    min_date_created = filters.DateFilter(
        field_name="date_created",
        lookup_expr='gte')

    max_date_created = filters.DateFilter(
        field_name="date_created",
        lookup_expr='lte')

    sort_by = filters.CharFilter(
        method='filter_sort_by',
    )

    def filter_sort_by(self, queryset, name, value):
        values = value.lower().split(',')
        return queryset.order_by(*values)

    class Meta:
        model = Contract
        fields = [
            'status',
            'sales_contact',
            'amount',
            'payment_due',
            'date_created',
            'date_updated',
            'min_date_created',
            'max_date_created',
            'sort_by'
        ]


class EventFilter(filters.FilterSet):
    min_date_created = filters.DateFilter(
        field_name="date_created",
        lookup_expr='gte')

    max_date_created = filters.DateFilter(
        field_name="date_created",
        lookup_expr='lte')

    notes_contains = filters.CharFilter(
        field_name="notes",
        lookup_expr='icontains'
    )

    sort_by = filters.CharFilter(
        method='filter_sort_by',
    )

    def filter_sort_by(self, queryset, name, value):
        values = value.lower().split(',')
        return queryset.order_by(*values)

    class Meta:
        model = Event
        fields = [
            'support_contact',
            'attendees',
            'notes',
            'event_date',
            'date_created',
            'date_updated',
            'min_date_created',
            'max_date_created',
            'sort_by'
        ]
