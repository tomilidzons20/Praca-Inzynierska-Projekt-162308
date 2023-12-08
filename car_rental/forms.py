from django import forms

from .models import Car
from .models import CarRental
from .models import CarMaintenance
from .utils import set_form_styles


class CarForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_form_styles(self.fields)

    class Meta:
        model = Car
        fields = '__all__'
        widgets = {
            'status': forms.Select(
                attrs={'class': 'form-select'},
            ),
            'car_picture': forms.FileInput(),
        }


class CarMaintenanceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_form_styles(self.fields)

    class Meta:
        model = CarMaintenance
        fields = '__all__'
        widgets = {
            'date_of_repair': forms.DateInput(
                format='YYYY-MM-DD',
                attrs={'type': 'date', 'required': True},
            ),
            'status': forms.Select(
                attrs={'class': 'form-select'},
            ),
            'car': forms.Select(
                attrs={'class': 'form-select'},
            ),
        }


class CarRentalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_form_styles(self.fields)

    class Meta:
        model = CarRental
        fields = '__all__'
        widgets = {
            'start_date': forms.DateTimeInput(
                format='YYYY-MM-DD',
                attrs={'type': 'datetime-local', 'required': True},
            ),
            'end_date': forms.DateTimeInput(
                format='YYYY-MM-DD',
                attrs={'type': 'datetime-local', 'required': True},
            ),
            'user': forms.Select(
                attrs={'class': 'form-select'},
            ),
            'car': forms.Select(
                attrs={'class': 'form-select'},
            ),
        }