# Generated by Django 5.1.6 on 2025-03-09 17:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('violations', '0010_remove_violationrecord_date_recorded'),
    ]

    operations = [
        migrations.AddField(
            model_name='violationrecord',
            name='previous_inspection',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='violationrecord',
            name='datetime_inspection',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
