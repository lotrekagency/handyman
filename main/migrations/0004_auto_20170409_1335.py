# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-09 13:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0003_auto_20170409_1245"),
    ]

    operations = [
        migrations.RenameField(
            model_name="project",
            old_name="password",
            new_name="server_address",
        ),
        migrations.RenameField(
            model_name="project",
            old_name="server",
            new_name="ssh_password",
        ),
        migrations.RenameField(
            model_name="project",
            old_name="username",
            new_name="ssh_username",
        ),
    ]
