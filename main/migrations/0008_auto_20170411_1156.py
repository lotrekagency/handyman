# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-11 09:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0007_project_backup_sync_folders"),
    ]

    operations = [
        migrations.CreateModel(
            name="Machine",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                (
                    "server_address",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "ssh_username",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "ssh_password",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                ("end_time", models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Reseller",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name="machine",
            name="reseller",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="main.Reseller",
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="machine",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="main.Machine",
            ),
        ),
    ]
