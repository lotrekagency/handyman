# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-06 10:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_auto_20180305_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='domain',
            name='own',
            field=models.NullBooleanField(choices=[(True, 'Yes'), (False, 'No')]),
        ),
    ]