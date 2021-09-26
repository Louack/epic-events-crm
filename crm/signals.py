from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Client


@receiver(post_save, sender=Client)
def sales_contact_modified_handler(instance, **kwargs):
    for contract in instance.contract_set.all():
        contract.sales_contact = instance.sales_contact
        contract.save()

