# Generated by Django 4.2.7 on 2023-12-28 10:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('car_rental', '0017_alter_carrental_extra'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CarLongTermRental',
        ),
    ]
