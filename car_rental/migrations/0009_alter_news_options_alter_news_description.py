# Generated by Django 4.2.7 on 2023-12-11 10:12

from django.db import migrations
import django_bleach.models


class Migration(migrations.Migration):

    dependencies = [
        ('car_rental', '0008_news_add_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'verbose_name': 'News', 'verbose_name_plural': 'News'},
        ),
        migrations.AlterField(
            model_name='news',
            name='description',
            field=django_bleach.models.BleachField(),
        ),
    ]
