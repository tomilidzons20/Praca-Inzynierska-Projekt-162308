from phonenumber_field.formfields import PhoneNumberField, RegionalPhoneNumberWidget
from allauth.account.forms import AddEmailForm
from allauth.account.forms import ChangePasswordForm
from allauth.account.forms import LoginForm
from allauth.account.forms import ResetPasswordForm
from allauth.account.forms import SignupForm

from django import forms
from django.utils.translation import gettext_lazy as _

from car_rental.utils import set_form_styles

from .models import Address
from .models import CustomUser


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_form_styles(self.fields)


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(
        label=_('First name'),
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': _('First name')}
        ),
    )
    last_name = forms.CharField(
        label=_('Last name'),
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': _('Last name')}
        ),
    )
    phone_number = PhoneNumberField(
        label=_('Phone number'),
        required=True,
        widget=RegionalPhoneNumberWidget(
            attrs={'placeholder': _('Phone number')}
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_form_styles(self.fields)

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.phone_number = self.cleaned_data.get('phone_number')
        user.save()
        return user


class CustomChangePasswordForm(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_form_styles(self.fields)


class CustomResetPasswordForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_form_styles(self.fields)


class CustomEmailForm(AddEmailForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_form_styles(self.fields)


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_form_styles(self.fields)

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'first_name',
            'last_name',
            'phone_number',
            'profile_picture',
        ]
        widgets = {
            'profile_picture': forms.FileInput(),
        }


class AddressForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_form_styles(self.fields)

    class Meta:
        model = Address
        fields = '__all__'
        exclude = [
            'account',
        ]
