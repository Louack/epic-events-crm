from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Manager


@receiver(post_save, sender=User)
def user_created_handler(instance, **kwargs):
    """
    Marks saved user as staff member.
    """
    if not instance.is_staff:
        instance.is_staff = True
        instance.save()


@receiver(post_save, sender=User)
def superuser_added_handler(instance, **kwargs):
    """
    Create a manager object when an associated saved user is a superuser.
    If not superuser, delete the associated manager object if any.
    """
    if instance.is_superuser:
        if not hasattr(instance, 'manager'):
            Manager.objects.create(user=instance)
    else:
        if hasattr(instance, 'manager'):
            instance.manager.delete()


@receiver(post_save, sender=Manager)
def manager_created_handler(instance, **kwargs):
    """
    Marks a user as a superuser when an associated manager object is created.
    """
    user = instance.user
    if not user.is_superuser:
        user.is_superuser = True
        user.save()


@receiver(post_delete, sender=Manager)
def manager_deleted_handler(instance, **kwargs):
    """
    Unmarks a user as a superuser when an associated manager object is deleted.
    """
    user = instance.user
    if user.is_superuser:
        user.is_superuser = False
        user.save()
