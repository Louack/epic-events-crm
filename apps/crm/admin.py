from django.contrib import admin

from apps.user_profiles.models import Salesman, Support
from .models import Client, Contract, Event


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None,
            {
                "fields": [
                    'sales_contact',
                ]
            }
        ),
        (
            'Personal info',
            {
                "fields": [
                    'last_name',
                    'first_name',
                    'email',
                    'phone',
                    'mobile',
                    'company',
                ]
            }
        ),
        (
            'Important dates',
            {
                "fields": [
                    'date_created',
                    'date_updated'
                ]
            }
        )
    ]

    list_display = [
        'id',
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

    readonly_fields = [
        'date_created',
        'date_updated'
    ]

    list_filter = [
        'sales_contact',
        'last_name',
    ]

    search_fields = [
        'last_name',
        'first_name',
        'email',
        'phone',
        'mobile',
        'company',
    ]

    ordering = ('id',)

    def has_view_permission(self, request, obj=None):
        if hasattr(request.user, 'manager'):
            return True
        elif hasattr(request.user, 'salesman') or hasattr(request.user, 'support'):
            return True

    def has_delete_permission(self, request, obj=None):
        if hasattr(request.user, 'manager'):
            return True
        elif hasattr(request.user, 'salesman') and obj:
            if request.user.salesman == obj.sales_contact:
                return True

    def has_change_permission(self, request, obj=None):
        if hasattr(request.user, 'manager'):
            return True
        elif hasattr(request.user, 'salesman') and obj:
            if request.user.salesman == obj.sales_contact:
                return True

    def has_add_permission(self, request):
        if hasattr(request.user, 'manager'):
            return True
        elif hasattr(request.user, 'salesman'):
            return True

    def has_module_permission(self, request):
        if hasattr(request.user, 'manager'):
            return True
        elif hasattr(request.user, 'salesman') or hasattr(request.user, 'support'):
            return True

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        lock the sales_contact field on the salesman in charge if request user is the salesman
        itself.
        Managers can have access to all salesmen and change the field at will.
        """
        if db_field.name == 'sales_contact' and hasattr(request.user, 'salesman'):
            kwargs["queryset"] = Salesman.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None,
            {
                "fields": [
                    'sales_contact',
                    'client'
                ]
            }
        ),
        (
            'Contract info',
            {
                "fields": [
                    'status',
                    'amount',
                    'payment_due',
                ]
            }
        ),
        (
            'Important dates',
            {
                "fields": [
                    'date_created',
                    'date_updated'
                ]
            }
        )
    ]

    readonly_fields = [
        'sales_contact',
        'date_created',
        'date_updated'
    ]

    list_display = [
        'id',
        'client',
        'sales_contact',
        'status',
        'amount',
        'payment_due',
        'date_created',
        'date_updated'
    ]

    list_filter = [
        'sales_contact',
        'client'
    ]

    ordering = ('id',)

    def has_view_permission(self, request, obj=None):
        if hasattr(request.user, 'manager'):
            return True
        elif hasattr(request.user, 'salesman') or hasattr(request.user, 'support'):
            return True

    def has_delete_permission(self, request, obj=None):
        if hasattr(request.user, 'manager'):
            return True
        elif hasattr(request.user, 'salesman') and obj:
            if request.user.salesman == obj.client.sales_contact:
                return True

    def has_change_permission(self, request, obj=None):
        if hasattr(request.user, 'manager'):
            return True
        elif hasattr(request.user, 'salesman') and obj:
            if request.user.salesman == obj.client.sales_contact:
                return True

    def has_add_permission(self, request):
        if hasattr(request.user, 'manager'):
            return True
        elif hasattr(request.user, 'salesman'):
            return True

    def has_module_permission(self, request):
        if hasattr(request.user, 'manager'):
            return True
        elif hasattr(request.user, 'salesman') or hasattr(request.user, 'support'):
            return True

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        For creation, display the clients that are part of the request user salesman.
        For change, lock the client linked to the contract.
        """
        if db_field.name == 'client':
            if 'add' in request.path and hasattr(request.user, 'salesman'):
                kwargs["queryset"] = Client.objects.filter(sales_contact=request.user.salesman)
            elif 'change' in request.path:
                obj_id = ''.join(num for num in request.path if num.isdigit())
                kwargs["queryset"] = Client.objects.filter(contract__id=obj_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.sales_contact = obj.client.sales_contact
        obj.save()


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None,
            {
                "fields": [
                    'support_contact',
                    'event_status',
                    'client'
                ]
            }
        ),
        (
            'Event info',
            {
                "fields": [
                    'attendees',
                    'notes',
                ]
            }
        ),
        (
            'Important dates',
            {
                "fields": [
                    'event_date',
                    'date_created',
                    'date_updated'
                ]
            }
        )
    ]

    readonly_fields = [
        'client',
        'date_created',
        'date_updated'
    ]

    list_display = [
        'id',
        'event_status',
        'client',
        'support_contact',
        'attendees',
        'notes',
        'event_date',
        'date_created',
        'date_updated'
        ]

    list_filter = [
        'event_status',
        'support_contact',
        'client',
        'event_date'
    ]

    ordering = ('id',)

    def has_view_permission(self, request, obj=None):
        if hasattr(request.user, 'manager'):
            return True
        elif hasattr(request.user, 'salesman') or hasattr(request.user, 'support'):
            return True

    def has_delete_permission(self, request, obj=None):
        if hasattr(request.user, 'manager'):
            return True
        elif hasattr(request.user, 'support') and obj:
            if request.user.support == obj.support_contact:
                return True

    def has_change_permission(self, request, obj=None):
        if hasattr(request.user, 'manager'):
            return True
        elif hasattr(request.user, 'support') and obj:
            if request.user.support == obj.support_contact:
                return True

    def has_add_permission(self, request):
        if hasattr(request.user, 'manager'):
            return True
        elif hasattr(request.user, 'salesman'):
            return True

    def has_module_permission(self, request):
        if hasattr(request.user, 'manager'):
            return True
        elif hasattr(request.user, 'salesman') or hasattr(request.user, 'support'):
            return True

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        If creation, display a list of contracts witout event  and under the control of the
        salesman if request user is a salesman. Display only the list of contracts without events
        if request user is manager.
        If change, lock the support_contact associated with the request user if it is a support
        and lock also the contract associated with the event.
        """
        if db_field.name == 'support_contact':
            if 'change' in request.path and hasattr(request.user, 'support'):
                kwargs["queryset"] = Support.objects.filter(user=request.user)
        elif db_field.name == 'event_status':
            if 'add' in request.path:
                if hasattr(request.user, 'salesman'):
                    kwargs["queryset"] = \
                        Contract.objects.filter(event=None,
                                                sales_contact=request.user.salesman)
                else:
                    kwargs["queryset"] = Contract.objects.filter(event=None)
            elif 'change' in request.path:
                obj_id = ''.join(num for num in request.path if num.isdigit())
                kwargs["queryset"] = Contract.objects.filter(event__id=obj_id, )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.client = obj.event_status.client
        obj.save()
