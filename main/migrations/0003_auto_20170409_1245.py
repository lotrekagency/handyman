# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-09 12:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0002_project_team"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="backup_archive",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="project",
            name="backup_script",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="project",
            name="password",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="project",
            name="server",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="project",
            name="slug",
            field=models.SlugField(default="", max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="project",
            name="username",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
