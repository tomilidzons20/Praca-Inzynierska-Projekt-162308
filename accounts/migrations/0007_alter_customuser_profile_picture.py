# Generated by Django 4.2.7 on 2024-01-13 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_customuser_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/img/profile_pictures', verbose_name='Profile picture'),
        ),
    ]
