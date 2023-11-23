from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField


def validate_year(value):
    current_year = timezone.now().year
    if value < 1900 or value > current_year:
        message = _('Year must be between 1900 and ')
        raise ValidationError(f'{message}{current_year}')


class Car(models.Model):
    class StatusChoices(models.TextChoices):
        AVAILABLE = 'AV', _('Available')
        UNAVAILABLE = 'UN', _('Unavailable')
        MAINTENANCE = 'MA', _('Maintenance')
        RENTED = 'RE', _('Rented')

    brand = models.CharField(
        _('Brand'),
        max_length=64,
        blank=False,
    )
    model = models.CharField(
        _('Model'),
        max_length=64,
        blank=False,
    )
    engine_capacity = models.CharField(
        _('Engine capacity'),
        blank=True,
    )
    engine_power = models.CharField(
        _('Engine power'),
        blank=True,
    )
    mileage = models.IntegerField(
        _('Mileage'),
        blank=True,
    )
    status = models.CharField(
        _('Status'),
        choices=StatusChoices.choices,
        default=StatusChoices.UNAVAILABLE,
    )
    production_year = models.PositiveIntegerField(
        _('Production year'),
        validators=[validate_year]
    )
    car_picture = models.ImageField(
        upload_to='uploads/img/car_pictures',
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.brand} {self.model} {self.production_year}'

    class Meta:
        verbose_name = _('Car')
        verbose_name_plural = _('Cars')


class CarMaintenance(models.Model):
    car = models.ForeignKey(
        'Car',
        verbose_name=_('Car'),
        on_delete=models.CASCADE,
    )
    date_of_repair = models.DateField(
        _('Date of repair'),
        default=timezone.now,
        blank=True,
    )
    cost_of_repair = MoneyField(
        _('Cost of repair'),
        max_digits=19,
        decimal_places=2,
        default_currency='PLN',
        default=0,
        blank=True,
    )

    def __str__(self):
        return f'{self.car}, {self.date_of_repair} {self.cost_of_repair}'

    class Meta:
        verbose_name = _('Car maintenance')
        verbose_name_plural = _('Car maintenance')


class CarRental(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
    )
    car = models.ForeignKey(
        'Car',
        verbose_name=_('Car'),
        on_delete=models.CASCADE,
    )
    start_date = models.DateTimeField(
        _('Start date of car rental'),
        blank=True,
    )
    end_date = models.DateTimeField(
        _('End date of car rental'),
        blank=True,
    )
    time_rented = models.DurationField(
        _('Total time of car rental'),
        blank=True,
        null=True,
    )
    car_mileage_start = models.IntegerField(
        _('Car mileage at start of car rental'),
        blank=True,
    )
    car_mileage_end = models.IntegerField(
        _('Car mileage at end of car rental'),
        blank=True,
    )
    car_mileage_change = models.IntegerField(
        _('Car mileage change'),
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        self.car_mileage_change = self.car_mileage_end - self.car_mileage_start
        if self.start_date and self.end_date:
            self.time_rented = self.end_date - self.start_date
        else:
            self.time_rented = None
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Car rental')
        verbose_name_plural = _('Car rentals')
