# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-06 18:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0030_machine_root_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machine',
            name='root_permissions',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False),
        ),
    ]
