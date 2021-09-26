from django.contrib import admin

from user_profiles.models import Salesman
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
        if db_field.name == 'sales_contact' and hasattr(request.user, 'salesman'):
            kwargs["queryset"] = Salesman.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


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
        if db_field.name == 'support_contact':
            if 'change' in request.path and hasattr(request.user, 'support'):
                kwargs["queryset"] = Support.objects.filter(user=request.user)
        elif db_field.name == 'event_status':
            if 'add' in request.path:
                if hasattr(request.user, 'salesman'):
                    kwargs["queryset"] = Contract.objects.filter(event=None,
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