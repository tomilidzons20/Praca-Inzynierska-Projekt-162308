from django.contrib import admin

from .models import Car
from .models import CarMaintenance
from .models import CarRental
from .models import News

from django.db import models
from ckeditor.widgets import CKEditorWidget


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
        'mileage',
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
        'car_mileage_change',
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
