import random

from django.db import models
from apps.user_profiles.models import Salesman, Support


class Client(models.Model):
    sales_contact = models.ForeignKey(
        to=Salesman,
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
    )
    first_name = models.CharField(
        max_length=25
    )
    last_name = models.CharField(
        max_length=25
    )
    email = models.EmailField(
        max_length=100
    )
    phone = models.CharField(
        max_length=20
    )
    mobile = models.CharField(
        max_length=20
    )
    company = models.CharField(
        max_length=25,
        null=True,
        blank=True
    )
    date_created = models.DateTimeField(
        auto_now_add=True
    )
    date_updated = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = 'Client'

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Contract(models.Model):
    sales_contact = models.ForeignKey(
        to=Salesman,
        on_delete=models.SET_NULL,
        blank=False,
        null=True
    )
    client = models.ForeignKey(
        to=Client,
        on_delete=models.SET_NULL,
        blank=False,
        null=True
    )
    status = models.BooleanField()
    amount = models.FloatField()
    payment_due = models.DateTimeField()
    date_created = models.DateTimeField(
        auto_now_add=True
    )
    date_updated = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = 'Contract'

    def __str__(self):
        return f'Contract n°{self.pk}'


class Event(models.Model):
    support_contact = models.ForeignKey(
        to=Support,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    client = models.ForeignKey(
        to=Client,
        on_delete=models.SET_NULL,
        blank=False,
        null=True
    )
    event_status = models.OneToOneField(
        to=Contract,
        on_delete=models.CASCADE,
        blank=False,
        null=True
    )
    attendees = models.IntegerField()
    notes = models.TextField()
    event_date = models.DateTimeField()
    date_created = models.DateTimeField(
        auto_now_add=True
    )
    date_updated = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = 'Event'

    def __str__(self):
        return f'Event n°{self.pk}'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.support_contact is None:
            self.support_contact = self.assign_default_support()
        super().save(force_insert=False, force_update=False, using=None,
                     update_fields=None)

    @staticmethod
    def assign_default_support():
        supports = Support.objects.all()
        potential_assignees = []
        min_events_assigned = None
        for support in supports:
            number_of_events_assigned = len(support.event_set.all())
            if not min_events_assigned:
                min_events_assigned = number_of_events_assigned
                potential_assignees = [support]
            elif min_events_assigned < number_of_events_assigned:
                pass
            elif min_events_assigned == number_of_events_assigned:
                potential_assignees.append(support)
            elif min_events_assigned > number_of_events_assigned:
                min_events_assigned = number_of_events_assigned
                potential_assignees = [support]
        if potential_assignees:
            assigned_support = random.choice(potential_assignees)
            return assigned_support
