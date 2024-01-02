from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Address
from .models import CustomUser


@admin.register(CustomUser)
class AdminCustomUser(UserAdmin):
    fieldsets = [
        (None, {'fields': (
             'username',
             'password',
        )}),
        (_('Personal info'), {'fields': (
             'first_name',
             'last_name',
             'email',
             'phone_number',
        )}),
        (_('Profile'), {'fields': (
            'profile_picture',
        )}),
        (_('Permissions'), {'fields': (
             'is_active',
             'is_staff',
             'is_superuser',
             'groups',
             'user_permissions',
        )}),
        (_('Important dates'), {'fields': (
             'last_login',
             'date_joined',
        )}),
    ]


@admin.register(Address)
class AdminAddress(admin.ModelAdmin):
    list_display = [
        'account',
        'first_name',
        'last_name',
        'city',
        'street',
        'building_number',
        'post_code',
    ]
    list_filter = [
        'account',
    ]
