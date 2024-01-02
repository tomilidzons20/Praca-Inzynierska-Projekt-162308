from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    phone_number = PhoneNumberField()
    profile_picture = models.ImageField(
        upload_to='uploads/img/profile_pictures',
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')


class Address(models.Model):
    account = models.OneToOneField(
        CustomUser,
        verbose_name=_('Account'),
        on_delete=models.CASCADE,
    )
    first_name = models.CharField(
        _('First name'),
        max_length=255,
        blank=False,
        null=False,
    )
    last_name = models.CharField(
        _('Last Name'),
        max_length=255,
        blank=False,
        null=False,
    )
    street = models.CharField(
        _('Street'),
        max_length=255,
        blank=True,
    )
    building_number = models.CharField(
        _('Building number'),
        max_length=255,
        blank=False,
        null=False,
    )
    post_code = models.CharField(
        _('Post code'),
        max_length=16,
        blank=False,
        null=False,
    )
    city = models.CharField(
        _('City'),
        max_length=255,
        blank=False,
        null=False,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.city} {self.street}'

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')
