from django import forms
from django.utils.translation import gettext_lazy as _
from django_filters import FilterSet
from django_filters.filters import ChoiceFilter
from django_filters.filters import ModelChoiceFilter
from django_filters.filters import OrderingFilter

from .models import Car
from .models import CarMaintenance


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
