# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-15 21:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0009_auto_20170614_2315"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lotrekuser",
            name="phone_number",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name="lotrekuser",
            name="twilio_account",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="lotrekuser",
            name="twilio_token",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
