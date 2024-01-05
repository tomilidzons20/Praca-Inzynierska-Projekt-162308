from django import forms
from django.utils.translation import gettext_lazy as _
from django_filters import FilterSet
from django_filters.filters import AllValuesFilter
from django_filters.filters import ChoiceFilter
from django_filters.filters import ModelChoiceFilter
from django_filters.filters import OrderingFilter

from accounts.models import CustomUser

from .models import Car
from .models import CarMaintenance
from .models import CarRental
from .models import ContactMessage
from .models import News


class MaintenanceFilter(FilterSet):
    car = ModelChoiceFilter(
        field_name='car',
        queryset=Car.objects.all(),
        empty_label=_('All'),
        widget=forms.Select(
            attrs={'class': 'form-select'},
        ),
    )
    status = ChoiceFilter(
        field_name='status',
        empty_label=_('All'),
        choices=CarMaintenance.MaintenanceChoices.choices,
        widget=forms.Select(
            attrs={'class': 'form-select'},
        ),
    )
    ordering = OrderingFilter(
        fields=(
            ('date_of_repair', 'date_of_repair'),
            ('cost_of_repair', 'cost_of_repair'),
        ),
        choices=(
            ('-date_of_repair', _('Date of repair (descending)')),
            ('date_of_repair', _('Date of repair')),
            ('-cost_of_repair', _('Cost of repair (descending)')),
            ('cost_of_repair', _('Cost of repair')),
        ),
        null_label=None,
        empty_label=None,
        label=_('Order by:'),
        widget=forms.Select,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['ordering'].field.widget.attrs.update({
            'class': 'form-select',
        })

    class Meta:
        model = CarMaintenance
        fields = [
            'car',
            'status',
        ]


class ContactFilter(FilterSet):
    user = ModelChoiceFilter(
        field_name='user',
        queryset=CustomUser.objects.all(),
        empty_label=_('All'),
        widget=forms.Select(
            attrs={'class': 'form-select'},
        ),
    )
    category = ChoiceFilter(
        field_name='category',
        empty_label=_('All'),
        choices=ContactMessage.CategoryChoices.choices,
        widget=forms.Select(
            attrs={'class': 'form-select'},
        ),
    )
    status = ChoiceFilter(
        field_name='status',
        empty_label=_('All'),
        choices=ContactMessage.StatusChoices.choices,
        widget=forms.Select(
            attrs={'class': 'form-select'},
        ),
    )
    ordering = OrderingFilter(
        fields=(
            ('add_date', _('Date of creation')),
        ),
        choices=(
            ('-add_date', _('Date of creation (descending)')),
            ('add_date', _('Date of creation')),
        ),
        null_label=None,
        empty_label=None,
        label=_('Order by:'),
        widget=forms.Select,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['ordering'].field.widget.attrs.update({
            'class': 'form-select',
        })

    class Meta:
        model = ContactMessage
        fields = [
            'user',
            'category',
            'status',
        ]


class CarRentalFilter(FilterSet):
    user = ModelChoiceFilter(
        field_name='user',
        queryset=CustomUser.objects.all(),
        empty_label=_('All'),
        widget=forms.Select(
            attrs={'class': 'form-select'},
        ),
    )
    car = ModelChoiceFilter(
        field_name='car',
        queryset=Car.objects.all(),
        empty_label=_('All'),
        widget=forms.Select(
            attrs={'class': 'form-select'},
        ),
    )
    status = ChoiceFilter(
        field_name='status',
        empty_label=_('All'),
        choices=CarRental.StatusChoices.choices,
        widget=forms.Select(
            attrs={'class': 'form-select'},
        ),
    )
    ordering = OrderingFilter(
        fields=(
            ('start_date', _('Start date')),
            ('end_date', _('End date')),
        ),
        choices=(
            ('-start_date', _('Start date (descending)')),
            ('start_date', _('Start date')),
            ('-end_date', _('End date (descending)')),
            ('end_date', _('End date')),
        ),
        null_label=None,
        empty_label=None,
        label=_('Order by:'),
        widget=forms.Select,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['ordering'].field.widget.attrs.update({
            'class': 'form-select',
        })

    class Meta:
        model = CarRental
        fields = [
            'user',
            'car',
            'status',
        ]


class NewsFilter(FilterSet):
    ordering = OrderingFilter(
        fields=(
            ('add_date', _('Date of creation')),
        ),
        choices=(
            ('-add_date', _('Date of creation (descending)')),
            ('add_date', _('Date of creation')),
        ),
        null_label=None,
        empty_label=None,
        label=_('Order by:'),
        widget=forms.Select,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['ordering'].field.widget.attrs.update({
            'class': 'form-select',
        })

    class Meta:
        model = News
        fields = ''


class CarFilter(FilterSet):
    brand = AllValuesFilter(
        field_name='brand',
        empty_label=_('All'),
        widget=forms.Select(
            attrs={'class': 'form-select'},
        ),
    )
    status = ChoiceFilter(
        field_name='status',
        empty_label=_('All'),
        choices=Car.StatusChoices.choices,
        widget=forms.Select(
            attrs={'class': 'form-select'},
        ),
    )
    ordering = OrderingFilter(
        fields=(
            ('day_cost', _('Day cost')),
        ),
        choices=(
            ('-day_cost', _('Day cost (descending)')),
            ('day_cost', _('Day cost')),
        ),
        null_label=None,
        empty_label=None,
        label=_('Order by:'),
        widget=forms.Select,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['ordering'].field.widget.attrs.update({
            'class': 'form-select',
        })

    class Meta:
        model = Car
        fields = [
            'brand',
            'status',
        ]
