from allauth.account.forms import LoginForm
from allauth.account.forms import SignupForm
from allauth.account.forms import ChangePasswordForm
from allauth.account.forms import ResetPasswordForm
from allauth.account.forms import AddEmailForm
from car_rental.utils import set_form_styles


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_form_styles(self.fields)


class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_form_styles(self.fields)


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
