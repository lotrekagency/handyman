# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-13 13:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0047_auto_20180313_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Customer'),
        ),
    ]