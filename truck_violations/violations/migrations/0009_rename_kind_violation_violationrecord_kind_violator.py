# Generated by Django 5.1.6 on 2025-03-06 17:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('violations', '0008_rename_license_number_violator_circulation_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='violationrecord',
            old_name='kind_violation',
            new_name='kind_violator',
        ),
    ]
