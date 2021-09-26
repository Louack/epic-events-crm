from django.contrib import admin

from .models import Salesman, Support, Manager


@admin.register(Salesman)
class SalesmanAdmin(admin.ModelAdmin):
    list_display = (
        'user',
    )

    def has_view_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True


@admin.register(Support)
class SalesmanAdmin(admin.ModelAdmin):
    list_display = (
        'user',
    )

    def has_view_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = (
        'user',
    )

    def has_view_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True
