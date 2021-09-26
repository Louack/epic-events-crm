from django.contrib import admin
from .models import Client, Contract, Event


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    fields = [
        'last_name',
        'first_name',
        'sales_contact',
        'email',
        'phone',
        'mobile',
        'company',
    ]

    list_display = [
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


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    fields = [
        'status',
        'client',
        'amount',
        'payment_due',
        'sales_contact',
        'date_created',
        'date_updated'
    ]

    readonly_fields = [
        'sales_contact',
        'date_created',
        'date_updated'
    ]

    list_display = [
        'status',
        'sales_contact',
        'client',
        'amount',
        'payment_due',
        'date_created',
        'date_updated'
    ]

    @admin.register(Event)
    class EventAdmin(admin.ModelAdmin):
        fields = [
            'event_status',
            'support_contact',
            'client',
            'attendees',
            'notes',
            'event_date',
            'date_created',
            'date_updated'
        ]

        readonly_fields = [
            'client',
            'date_created',
            'date_updated'
        ]

        list_display = [
            'event_status',
            'support_contact',
            'client',
            'attendees',
            'notes',
            'event_date',
            'date_created',
            'date_updated'
            ]
