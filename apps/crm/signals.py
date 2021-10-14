from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Client


@receiver(post_save, sender=Client)
def sales_contact_modified_handler(instance, **kwargs):
    """
    Replaces a contract sales_contact with the modified sales_contact of its corresponding client.
    """
    for contract in instance.contract_set.all():
        if contract.sales_contact != instance.sales_contact:
            contract.sales_contact = instance.sales_contact
            contract.save()
