from django.db import models
from django.contrib.auth.models import User


class Salesman(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )

    class Meta:
        verbose_name = 'Salesman'

    def __str__(self):
        return self.user.username


class Support(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )

    class Meta:
        verbose_name = 'Support'

    def __str__(self):
        return self.user.username


class Manager(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )

    class Meta:
        verbose_name = 'Manager'

    def __str__(self):
        return self.user.username
