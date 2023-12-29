from django import forms
from django.utils.translation import gettext_lazy as _
from django_filters import FilterSet
from django_filters.filters import ChoiceFilter
from django_filters.filters import ModelChoiceFilter
from django_filters.filters import OrderingFilter

from accounts.models import CustomUser
from .models import Car
from .models import CarRental
from .models import CarMaintenance
from .models import ContactMessage


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
            ('date_of_repair', _('Date of repair')),
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
        order_by = (
            ('date_of_repair', _('Date of repair')),
            ('cost_of_repair', _('Cost of repair')),
        )


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
            ('end_date', _('End date'))
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
