from math import ceil

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django_bleach.models import BleachField
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
        verbose_name=_('Car picture'),
        blank=True,
        null=True,
    )
    day_cost = MoneyField(
        _('Cost of one day rental'),
        max_digits=19,
        decimal_places=2,
        default_currency='PLN',
        default=0,
        blank=True,
    )

    def __str__(self):
        return f'{self.brand} {self.model} {self.production_year}'

    class Meta:
        verbose_name = _('Car')
        verbose_name_plural = _('Cars')


class CarMaintenance(models.Model):
    class MaintenanceChoices(models.TextChoices):
        INREPAIR = 'IR', _('In repair')
        DONE = 'DO', _('Done')
        SCHEDULED = 'SCH', _('Scheduled')

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
    status = models.CharField(
        _('Status'),
        choices=MaintenanceChoices.choices,
        default=MaintenanceChoices.SCHEDULED,
    )

    def save(self, *args, **kwargs):
        today = timezone.now().date()
        if self.car and today == self.date_of_repair:
            match self.status:
                case self.MaintenanceChoices.INREPAIR:
                    self.car.status = Car.StatusChoices.MAINTENANCE
                case self.MaintenanceChoices.DONE:
                    self.car.status = Car.StatusChoices.AVAILABLE
            self.car.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.car}, {self.date_of_repair} {self.cost_of_repair}'

    class Meta:
        verbose_name = _('Car maintenance')
        verbose_name_plural = _('Car maintenance')


class CarRental(models.Model):
    class StatusChoices(models.TextChoices):
        RESERVED = 'RS', _('Reserved')
        RENTED = 'RE', _('Rented')
        CLOSED = 'CL', _('Closed')
        CANCELLED = 'CA', _('Cancelled')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        null=True,
    )
    address = models.ForeignKey(
        'RentalAddress',
        verbose_name=_('Address'),
        on_delete=models.CASCADE,
        null=True,
    )
    car = models.ForeignKey(
        'Car',
        verbose_name=_('Car'),
        on_delete=models.CASCADE,
    )
    protection = models.ForeignKey(
        'RentalProtection',
        verbose_name=_('Protection'),
        on_delete=models.CASCADE,
        null=True,
    )
    extra = models.ManyToManyField(
        'RentalExtra',
        verbose_name=_('Extra'),
        blank=True,
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
    total_cost = MoneyField(
        _('Cost of rental'),
        max_digits=19,
        decimal_places=2,
        default_currency='PLN',
        default=0,
        blank=True,
    )
    status = models.CharField(
        _('Status'),
        choices=StatusChoices.choices,
        default=StatusChoices.RESERVED,
    )

    def save(self, *args, **kwargs):
        if self.start_date and self.end_date:
            self.time_rented = self.end_date - self.start_date
        else:
            self.time_rented = None
        today = timezone.now()
        if self.car and self.start_date <= today <= self.end_date:
            match self.status:
                case self.StatusChoices.RENTED:
                    self.car.status = Car.StatusChoices.RENTED
                case self.StatusChoices.CANCELLED | self.StatusChoices.CLOSED:
                    self.car.status = Car.StatusChoices.AVAILABLE
            self.car.save()
        # on update
        if self.id:
            self.total_cost = self.get_total_cost()
        super().save(*args, **kwargs)

    def get_total_cost(self):
        rental_days = ceil(((self.end_date - self.start_date).total_seconds() / 3600) / 24)
        extras_cost = sum([extra.cost for extra in self.extra.all()])
        return self.protection.cost + extras_cost + self.car.day_cost * rental_days

    def __str__(self):
        return f'{self.user} {self.car} {self.total_cost} {self.start_date} - {self.end_date}'

    class Meta:
        verbose_name = _('Car rental')
        verbose_name_plural = _('Car rentals')


class News(models.Model):
    title = models.CharField(
        _('Title'),
        max_length=128,
        blank=False,
        null=False,
    )
    description = BleachField(
        _('Description'),
    )
    main_picture = models.ImageField(
        upload_to='uploads/img/news',
        verbose_name=_('Main picture'),
        blank=True,
        null=True,
    )
    slug = models.SlugField(
        max_length=140,
        null=False,
    )
    add_date = models.DateTimeField(
        _('Add date'),
        default=timezone.now,
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = _('News')
        verbose_name_plural = _('News')


class RentalProtection(models.Model):
    name = models.CharField(
        _('Protection name'),
        max_length=64,
        blank=False,
        null=False,
    )
    tpl_insurance = models.BooleanField(
        _('Third party liability insurance'),
        null=False,
        blank=False,
    )
    wheel_protection = models.BooleanField(
        _('Tires and rims protection'),
        null=False,
        blank=False,
    )
    window_protection = models.BooleanField(
        _('Window protection'),
        null=False,
        blank=False,
    )
    cost = MoneyField(
        _('Protection cost'),
        max_digits=19,
        decimal_places=2,
        default_currency='PLN',
        default=0,
        blank=False,
    )
    penalty = MoneyField(
        _('Penalty cost'),
        max_digits=19,
        decimal_places=0,
        default_currency='PLN',
        default=0,
        blank=False,
    )
    deposit = MoneyField(
        _('Deposit cost'),
        max_digits=19,
        decimal_places=0,
        default_currency='PLN',
        default=0,
        blank=False,
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Rental protection')
        verbose_name_plural = _('Rental protections')


class RentalExtra(models.Model):
    name = models.CharField(
        _('Extra name'),
        max_length=64,
        blank=False,
        null=False,
    )
    cost = MoneyField(
        _('Extra cost'),
        max_digits=19,
        decimal_places=2,
        default_currency='PLN',
        default=0,
        blank=False,
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Rental extra')
        verbose_name_plural = _('Rental extras')


class RentalAddress(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        null=True,
    )
    first_name = models.CharField(
        _('First name'),
        max_length=255,
        blank=False,
        null=False,
    )
    last_name = models.CharField(
        _('Last name'),
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
        verbose_name = _('Rental address')
        verbose_name_plural = _('Rental addresses')


class ContactMessage(models.Model):
    class StatusChoices(models.TextChoices):
        NEW = 'NE', _('New')
        CLOSED = 'CL', _('Closed')

    class CategoryChoices(models.TextChoices):
        ACCIDENT = 'AC', _('Accident')
        BREAKDOWN = 'BR', _('Breakdown')
        QUESTION = 'QU', _('Question')
        COMPLAINT = 'CO', _('Complaint')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        null=True,
    )
    category = models.CharField(
        _('Category'),
        choices=CategoryChoices.choices,
        default=CategoryChoices.QUESTION,
    )
    message = models.TextField(
        _('Message'),
        blank=False
    )
    status = models.CharField(
        _('Status'),
        choices=StatusChoices.choices,
        default=StatusChoices.NEW,
    )
    add_date = models.DateTimeField(
        _('Date of contact message creation'),
        blank=True,
    )

    def __str__(self):
        return f'{self.user} {self.category} {self.status} {self.add_date}'

    class Meta:
        verbose_name = _('Contact message')
        verbose_name_plural = _('Contact messages')
