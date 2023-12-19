from ckeditor.widgets import CKEditorWidget
from django.contrib import admin
from django.db import models

from .models import Car
from .models import CarLongTermRental
from .models import CarMaintenance
from .models import CarRental
from .models import ContactMessage
from .models import News
from .models import RentalAddress
from .models import RentalExtra
from .models import RentalProtection


@admin.register(Car)
class AdminCar(admin.ModelAdmin):
    list_display = [
        'brand',
        'model',
        'production_year',
        'status',
    ]
    list_filter = [
        'brand',
        'model',
        'production_year',
        'status',
        'engine_power',
        'engine_capacity'
    ]


@admin.register(CarRental)
class AdminCarRental(admin.ModelAdmin):
    list_display = [
        'start_date',
        'end_date',
        'user',
        'car',
    ]
    list_filter = [
        'user',
        'car',
        'start_date',
        'end_date',
    ]
    readonly_fields = [
        'time_rented',
    ]


@admin.register(CarMaintenance)
class AdminCarMaintenance(admin.ModelAdmin):
    list_display = [
        'car',
        'date_of_repair',
        'cost_of_repair',
    ]
    list_filter = [
        'car',
    ]


@admin.register(News)
class AdminNews(admin.ModelAdmin):
    list_display = [
        'title',
        'add_date',
    ]
    readonly_fields = [
        'slug',
    ]
    list_filter = [
        'title',
        'add_date',
    ]
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }


@admin.register(RentalExtra)
class AdminRentalExtra(admin.ModelAdmin):
    list_display = [
        'name',
        'cost',
    ]
    list_filter = [
        'name',
        'cost',
    ]


@admin.register(RentalProtection)
class AdminRentalProtection(admin.ModelAdmin):
    list_display = [
        'name',
    ]
    list_filter = [
        'name',
    ]


@admin.register(RentalAddress)
class AdminRentalAddress(admin.ModelAdmin):
    list_display = ([
        'first_name',
    ])


@admin.register(ContactMessage)
class AdminContactMessage(admin.ModelAdmin):
    list_display = [
        'user',
        'status',
        'category',
    ]
    list_filter = [
        'user',
        'status',
        'category',
    ]


@admin.register(CarLongTermRental)
class AdminCarLongTermRental(admin.ModelAdmin):
    list_display = [
        'user',
        'start_date',
        'number_of_months',
        'status',
    ]
    list_filter = [
        'user',
        'start_date',
        'number_of_months',
        'status',
    ]
