from django.contrib import admin

from .models import Salesman, Support, Manager


@admin.register(Salesman)
class SalesmanAdmin(admin.ModelAdmin):
    list_display = (
        'user',
    )


@admin.register(Support)
class SalesmanAdmin(admin.ModelAdmin):
    list_display = (
        'user',
    )


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = (
        'user',
    )
