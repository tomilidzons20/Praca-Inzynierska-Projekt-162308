from django import forms

from .utils import set_form_styles
from .models import Car


class CarForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_form_styles(self.fields)

    class Meta:
        model = Car
        fields = '__all__'
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
