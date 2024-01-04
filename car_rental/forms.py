from ckeditor.widgets import CKEditorWidget
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import Car
from .models import CarMaintenance
from .models import CarRental
from .models import ContactMessage
from .models import News
from .models import RentalAddress
from .models import RentalExtra
from .models import RentalProtection
from .utils import set_form_styles

MINIMUM_HOURS_BEFORE_RENT = getattr(settings, "MINIMUM_HOURS_BEFORE_RENT", 3)
MINIMUM_RENT_HOURS = getattr(settings, "MINIMUM_RENT_HOURS", 3)


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
                format='%Y-%m-%d',
                attrs={'type': 'date', 'required': True},
            ),
            'status': forms.Select(
                attrs={'class': 'form-select'},
            ),
            'car': forms.Select(
                attrs={'class': 'form-select'},
            ),
        }


class CarMaintenanceUpdateForm(CarMaintenanceForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['car'].disabled = True


class CarRentalForm(forms.ModelForm):
    def clean(self):
        data = self.cleaned_data
        date_from = data.get('start_date')
        date_to = data.get('end_date')

        if date_to <= date_from:
            raise forms.ValidationError(_('End date must be later than start date.'))

        date_diff_hours = (date_to - date_from).total_seconds() // 3600
        if date_diff_hours < MINIMUM_RENT_HOURS:
            raise forms.ValidationError(
                _('Minimum rent time is ') + str(MINIMUM_RENT_HOURS) + _(' hour/s')
            )

        return data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_form_styles(self.fields)
        self.fields['address'].required = False

    class Meta:
        model = CarRental
        fields = '__all__'
        widgets = {
            'start_date': forms.DateTimeInput(
                format='%Y-%m-%d %H:%M',
                attrs={'type': 'datetime-local', 'required': True},
            ),
            'end_date': forms.DateTimeInput(
                format='%Y-%m-%d %H:%M',
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


class CarRentalUpdateForm(CarRentalForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].disabled = True
        self.fields['address'].disabled = True


class NewsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_form_styles(self.fields)

    class Meta:
        model = News
        fields = '__all__'
        widgets = {
            'main_picture': forms.FileInput(),
            'add_date': forms.DateTimeInput(
                format='%Y-%m-%d %H:%M',
                attrs={'type': 'datetime-local', 'required': True},
            ),
            'description': CKEditorWidget(),
        }
        exclude = [
            'slug',
        ]


class CarDaysRentalForm(forms.Form):
    date_from = forms.DateTimeField(
        label=_('Date from'),
        required=True,
        widget=forms.DateTimeInput(
            format='%Y-%m-%d %H:%M',
            attrs={'type': 'datetime-local'}
        )
    )
    date_to = forms.DateTimeField(
        label=_('Date to'),
        required=True,
        widget=forms.DateTimeInput(
            format='%Y-%m-%d %H:%M',
            attrs={'type': 'datetime-local'}
        )
    )

    def clean(self):
        data = self.cleaned_data
        date_from = data.get('date_from')
        date_to = data.get('date_to')

        if date_to <= date_from:
            raise forms.ValidationError(_('Date to must be later than date from.'))

        now = timezone.now()
        if date_from < now:
            raise forms.ValidationError(_('Date from cannot be in the past.'))

        if date_to < now:
            raise forms.ValidationError(_('Date to cannot be in the past.'))

        if date_from < now + timezone.timedelta(hours=MINIMUM_HOURS_BEFORE_RENT):
            raise forms.ValidationError(
                _('Date from not earlier than in ') + str(MINIMUM_HOURS_BEFORE_RENT) + _(' hours')
            )

        date_diff_hours = (date_to - date_from).total_seconds() // 3600
        if date_diff_hours < 1:
            raise forms.ValidationError(
                _('Minimum rent time is ') + str(MINIMUM_RENT_HOURS) + _(' hour/s')
            )

        return data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_form_styles(self.fields)
        self.fields['date_from'].initial = timezone.now() + timezone.timedelta(
            hours=MINIMUM_HOURS_BEFORE_RENT,
            minutes=30
        )
        self.fields['date_to'].initial = timezone.now() + timezone.timedelta(
            days=1,
            hours=MINIMUM_HOURS_BEFORE_RENT,
            minutes=30
        )


class CarChoiceForm(forms.Form):
    car = forms.ModelChoiceField(
        label=_('Car'),
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
        label=_('Use profile address'),
        widget=forms.CheckboxInput(),
        required=False,
    )

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        set_form_styles(self.fields)
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['building_number'].required = False
        self.fields['post_code'].required = False
        self.fields['city'].required = False

    def clean(self):
        data = self.cleaned_data
        if data.get('use_profile_address'):
            if hasattr(self.request.user, 'address'):
                return data
            else:
                raise ValidationError(_('You don\'t have saved profile address.'))
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


class ContactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_form_styles(self.fields)

    class Meta:
        model = ContactMessage
        fields = '__all__'
        widgets = {
            'user': forms.Select(
                attrs={'class': 'form-select'},
            ),
            'category': forms.Select(
                attrs={'class': 'form-select'},
            ),
            'status': forms.Select(
                attrs={'class': 'form-select'},
            ),
            'message': forms.Textarea(
                attrs={'style': 'height: 300px;'},
            ),
            'add_date': forms.DateTimeInput(
                format='%Y-%m-%d %H:%M',
                attrs={'type': 'datetime-local', 'required': True},
            ),
        }


class RentalProtectionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_form_styles(self.fields)

    class Meta:
        model = RentalProtection
        fields = '__all__'
        widgets = {
            'tpl_insurance': forms.CheckboxInput(
                attrs={'class': 'form-check-input'},
            ),
            'wheel_protection': forms.CheckboxInput(
                attrs={'class': 'form-check-input'},
            ),
            'window_protection': forms.CheckboxInput(
                attrs={'class': 'form-check-input'},
            ),
        }


class RentalExtraForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_form_styles(self.fields)

    class Meta:
        model = RentalExtra
        fields = '__all__'
