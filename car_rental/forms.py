from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import Car
from .models import CarLongTermRental
from .models import CarMaintenance
from .models import CarRental
from .models import ContactMessage
from .models import News
from .models import RentalAddress
from .models import RentalExtra
from .models import RentalProtection
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
    def clean(self):
        data = self.cleaned_data
        date_from = data.get('start_date')
        date_to = data.get('end_date')

        if date_to <= date_from:
            raise forms.ValidationError(_('Date to must be later than date from.'))

        date_diff_hours = (date_to - date_from).total_seconds() // 3600
        if date_diff_hours < 1:
            raise forms.ValidationError(_('Minimum rent time is 1 hour'))

        return data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_form_styles(self.fields)

    class Meta:
        model = CarRental
        fields = '__all__'
        widgets = {
            'start_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'required': True},
            ),
            'end_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'required': True},
            ),
            'user': forms.Select(
                attrs={'class': 'form-select'},
            ),
            'address': forms.Select(
                attrs={'class': 'form-select'},
            ),
            'car': forms.Select(
                attrs={'class': 'form-select'},
            ),
            'extra': forms.SelectMultiple(
                attrs={'class': 'form-select'},
            ),
            'protection': forms.Select(
                attrs={'class': 'form-select'},
            ),
            'status': forms.Select(
                attrs={'class': 'form-select'},
            ),
        }


class NewsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_form_styles(self.fields)

    class Meta:
        model = News
        fields = '__all__'
        widgets = {
            'main_picture': forms.FileInput(),
        }


class CarDaysRentalForm(forms.Form):
    date_from = forms.DateTimeField(
        required=True,
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'}
        )
    )
    date_to = forms.DateTimeField(
        required=True,
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'}
        )
    )

    def clean(self):
        data = self.cleaned_data
        date_from = data.get('date_from')
        date_to = data.get('date_to')
        minimum_hours_difference = 6

        if date_to <= date_from:
            raise forms.ValidationError(_('Date to must be later than date from.'))

        now = timezone.now()
        if date_from < now:
            raise forms.ValidationError(_('Date from cannot be in the past.'))

        if date_to < now:
            raise forms.ValidationError(_('Date to cannot be in the past.'))

        if date_from < now + timezone.timedelta(hours=minimum_hours_difference):
            raise forms.ValidationError(
                _('Date from not earlier than in ') + str(minimum_hours_difference) + _(' hours')
            )

        date_diff_hours = (date_to - date_from).total_seconds() // 3600
        if date_diff_hours < 1:
            raise forms.ValidationError(_('Minimum rent time is 1 hour'))

        return data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_form_styles(self.fields)


class CarChoiceForm(forms.Form):
    car = forms.ModelChoiceField(
        queryset=Car.objects.none(),
        required=True,
        widget=forms.RadioSelect(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_form_styles(self.fields)


class CarExtraForm(forms.Form):
    protection = forms.ModelChoiceField(
        queryset=RentalProtection.objects.all(),
        required=True,
        widget=forms.RadioSelect(),
        initial=1,
    )
    extra = forms.ModelMultipleChoiceField(
        queryset=RentalExtra.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_form_styles(self.fields)


class CarAddressForm(forms.ModelForm):
    use_profile_address = forms.BooleanField(
        widget=forms.CheckboxInput(),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_form_styles(self.fields)
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['building_number'].required = False
        self.fields['post_code'].required = False
        self.fields['city'].required = False

    def clean(self):
        data = self.cleaned_data
        if data.get('use_profile_address'):
            return data
        if (
            data.get('first_name') and
            data.get('last_name') and
            data.get('building_number') and
            data.get('post_code') and
            data.get('city')
        ):
            return data
        else:
            raise ValidationError(_('Please provide all address information.'))

    class Meta:
        model = RentalAddress
        fields = '__all__'
        exclude = [
            'user',
        ]


class RentalReviewForm(forms.Form):
    pass


class ClientContactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_form_styles(self.fields)

    class Meta:
        model = ContactMessage
        fields = '__all__'
        exclude = [
            'user',
            'status',
        ]
        widgets = {
            'category': forms.Select(
                attrs={'class': 'form-select'},
            ),
            'message': forms.Textarea(
                attrs={'style': 'height: 300px;'},
            ),
        }


class CarLongTermRentalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_form_styles(self.fields)

    def clean(self):
        data = self.cleaned_data
        start_date = data.get('start_date')
        minimum_hours_difference = 6

        now = timezone.now()
        if start_date < now:
            raise forms.ValidationError(_('Date from cannot be in the past.'))

        if start_date < now + timezone.timedelta(hours=minimum_hours_difference):
            raise forms.ValidationError(
                _('Date from not earlier than in ') + str(minimum_hours_difference) + _(' hours')
            )

        return data

    class Meta:
        model = CarLongTermRental
        fields = '__all__'
        exclude = [
            'user',
            'status',
        ]
        widgets = {
            'start_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
            ),
            'message': forms.Textarea(
                attrs={'style': 'height: 300px;'},
            ),
        }
