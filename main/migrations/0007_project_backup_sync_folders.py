# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-10 19:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0006_report_class_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="backup_sync_folders",
            field=models.TextField(blank=True, null=True),
        ),
    ]
