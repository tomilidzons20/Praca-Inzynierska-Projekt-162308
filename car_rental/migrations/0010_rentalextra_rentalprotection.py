# Generated by Django 4.2.7 on 2023-12-12 13:56

from decimal import Decimal
from django.db import migrations, models
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('car_rental', '0009_alter_news_options_alter_news_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='RentalExtra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Extra name')),
                ('cost_currency', djmoney.models.fields.CurrencyField(choices=[('PLN', 'Polish Zloty')], default='PLN', editable=False, max_length=3)),
                ('cost', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=19, verbose_name='Extra cost')),
            ],
            options={
                'verbose_name': 'Rental extra',
                'verbose_name_plural': 'Rental extras',
            },
        ),
        migrations.CreateModel(
            name='RentalProtection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Protection name')),
                ('tpl_insurance', models.BooleanField(verbose_name='Third party liability insurance')),
                ('wheel_protection', models.BooleanField(verbose_name='Tires and rims protection')),
                ('window_protection', models.BooleanField(verbose_name='Window protection')),
                ('cost_currency', djmoney.models.fields.CurrencyField(choices=[('PLN', 'Polish Zloty')], default='PLN', editable=False, max_length=3)),
                ('cost', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='PLN', max_digits=19, verbose_name='Protection cost')),
                ('penalty_currency', djmoney.models.fields.CurrencyField(choices=[('PLN', 'Polish Zloty')], default='PLN', editable=False, max_length=3)),
                ('penalty', djmoney.models.fields.MoneyField(decimal_places=0, default=Decimal('0'), default_currency='PLN', max_digits=19, verbose_name='Penalty cost')),
                ('deposit_currency', djmoney.models.fields.CurrencyField(choices=[('PLN', 'Polish Zloty')], default='PLN', editable=False, max_length=3)),
                ('deposit', djmoney.models.fields.MoneyField(decimal_places=0, default=Decimal('0'), default_currency='PLN', max_digits=19, verbose_name='Deposit cost')),
            ],
            options={
                'verbose_name': 'Rental protection',
                'verbose_name_plural': 'Rental protections',
            },
        ),
    ]
