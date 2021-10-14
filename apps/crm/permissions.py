from rest_framework.permissions import BasePermission


class IsManager(BasePermission):
    """
    Automatically grants access if request user is a manager.
    """
    def has_permission(self, request, view):
        if hasattr(request.user, 'manager'):
            return True

    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'manager'):
            return True


class ClientAccess(BasePermission):
    """
    Defines access at the client level.
    """
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return hasattr(request.user, 'salesman') or hasattr(request.user, 'support')
        else:
            return hasattr(request.user, 'salesman')

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return hasattr(request.user, 'salesman') or hasattr(request.user, 'support')
        else:
            if hasattr(request.user, 'salesman'):
                return request.user.salesman == obj.sales_contact


class ContractAccess(BasePermission):
    """
    Defines access at the contract level.
    """
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return hasattr(request.user, 'salesman') or hasattr(request.user, 'support')
        else:
            if hasattr(request.user, 'salesman'):
                return request.user.salesman == view.client.sales_contact

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return hasattr(request.user, 'salesman') or hasattr(request.user, 'support')
        else:
            if hasattr(request.user, 'salesman'):
                return request.user.salesman == obj.sales_contact


class EventAccess(BasePermission):
    """
    Defines access at the event level.
    """
    def has_permission(self, request, view):
        if view.action == 'create':
            if hasattr(request.user, 'salesman'):
                return request.user.salesman == view.contract.sales_contact
        elif view.action in ['list', 'retrieve']:
            return hasattr(request.user, 'salesman') or hasattr(request.user, 'support')
        else:
            return hasattr(request.user, 'support')

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return hasattr(request.user, 'salesman') or hasattr(request.user, 'support')
        else:
            if hasattr(request.user, 'support'):
                return request.user.support == obj.support_contact
