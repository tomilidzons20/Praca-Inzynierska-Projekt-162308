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
        null=True,
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
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Car rental')
        verbose_name_plural = _('Car rentals')


class News(models.Model):
    title = models.CharField(
        max_length=128,
        blank=False,
        null=False,
    )
    description = BleachField()
    main_picture = models.ImageField(
        upload_to='uploads/img/news',
        blank=True,
        null=True,
    )
    slug = models.SlugField(
        max_length=140,
        null=False,
    )
    add_date = models.DateField(
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
    )
    last_name = models.CharField(
        _('Last Name'),
        max_length=255,
    )
    street = models.CharField(
        _('Street'),
        max_length=255,
        blank=True,
    )
    building_number = models.CharField(
        _('Building number'),
        max_length=255,
    )
    post_code = models.CharField(
        _('Post code'),
        max_length=16,
    )
    city = models.CharField(
        _('City'),
        max_length=255,
    )

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

    class Meta:
        verbose_name = _('Contact message')
        verbose_name_plural = _('Contact messages')


class CarLongTermRental(models.Model):
    class StatusChoices(models.TextChoices):
        NEW = 'NE', _('New')
        IN_PROGRESS = 'IP', _('In progress')
        CLOSED = 'CL', _('Closed')
        CANCELLED = 'CA', _('Cancelled')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        null=True,
    )
    start_date = models.DateTimeField(
        _('Start date of car rental'),
        blank=False,
    )
    number_of_months = models.PositiveIntegerField(
        _('Number of months'),
        blank=False
    )
    message = models.TextField(
        _('Message'),
        blank=False,
    )
    status = models.CharField(
        _('Status'),
        choices=StatusChoices.choices,
        default=StatusChoices.NEW,
    )

    class Meta:
        verbose_name = _('Long term rental')
        verbose_name_plural = _('Long term rentals')
