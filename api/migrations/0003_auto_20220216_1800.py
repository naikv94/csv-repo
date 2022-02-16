# Generated by Django 2.2.6 on 2022-02-16 12:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_file_csv_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='csv_file',
            field=models.FileField(upload_to='', validators=[django.core.validators.FileExtensionValidator(['csv'])]),
        ),
    ]