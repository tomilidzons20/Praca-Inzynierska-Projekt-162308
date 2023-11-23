from django import forms

from .utils import set_form_styles
from .models import Car
from .models import CarMaintenance


class CarForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_form_styles(self.fields)

    class Meta:
        model = Car
        fields = '__all__'
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'car_picture': forms.FileInput(),
        }


class CarMaintenanceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_form_styles(self.fields)

    class Meta:
        model = CarMaintenance
        fields = [
            'date_of_repair',
            'cost_of_repair',
        ]
        widgets = {
            'date_of_repair': forms.DateInput(format='YYYY-MM-DD', attrs={'type': 'date', 'required': True}),
        }
