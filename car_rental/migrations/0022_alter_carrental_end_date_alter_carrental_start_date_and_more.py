# Generated by Django 4.2.7 on 2024-01-04 15:36

import car_rental.models
from decimal import Decimal
from django.db import migrations, models
import django.utils.timezone
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('car_rental', '0021_alter_rentaladdress_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrental',
            name='end_date',
            field=models.DateTimeField(default=car_rental.models.day_difference, verbose_name='End date of car rental'),
        ),
        migrations.AlterField(
            model_name='carrental',
            name='start_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Start date of car rental'),
        ),
        migrations.AlterField(
            model_name='contactmessage',
            name='add_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date of contact message creation'),
        ),
        migrations.AlterField(
            model_name='rentalprotection',
            name='cost',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=19, verbose_name='Protection cost:'),
        ),
        migrations.AlterField(
            model_name='rentalprotection',
            name='deposit',
            field=djmoney.models.fields.MoneyField(decimal_places=0, default=Decimal('0'), default_currency='PLN', max_digits=19, verbose_name='Deposit cost:'),
        ),
        migrations.AlterField(
            model_name='rentalprotection',
            name='name',
            field=models.CharField(max_length=64, verbose_name='Protection name:'),
        ),
        migrations.AlterField(
            model_name='rentalprotection',
            name='penalty',
            field=djmoney.models.fields.MoneyField(decimal_places=0, default=Decimal('0'), default_currency='PLN', max_digits=19, verbose_name='Penalty cost:'),
        ),
        migrations.AlterField(
            model_name='rentalprotection',
            name='tpl_insurance',
            field=models.BooleanField(verbose_name='Third party liability insurance:'),
        ),
        migrations.AlterField(
            model_name='rentalprotection',
            name='wheel_protection',
            field=models.BooleanField(verbose_name='Tires and rims protection:'),
        ),
        migrations.AlterField(
            model_name='rentalprotection',
            name='window_protection',
            field=models.BooleanField(verbose_name='Window protection:'),
        ),
    ]