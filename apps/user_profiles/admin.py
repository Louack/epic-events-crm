from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group

from .models import Salesman, Support, Manager

admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    def has_view_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True

    def get_fieldsets(self, request, obj=None):
        if not request.user.is_superuser:
            fieldsets = [
                (
                    None,
                    {
                        "fields": [
                            'username'
                        ]
                    }
                ),
                (
                    'Personal info',
                    {
                        "fields": [
                            'first_name',
                            'last_name',
                            'email'
                        ]
                    }
                )
            ]
            return fieldsets
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)


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
class SupportAdmin(admin.ModelAdmin):
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
