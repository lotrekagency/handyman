# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-07-24 13:43
from __future__ import unicode_literals

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_project_domain'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='managed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='lotrekuser',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
        ),
        migrations.AlterField(
            model_name='project',
            name='domain',
            field=models.CharField(default=True, max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='report',
            name='class_type',
            field=models.CharField(blank=True, choices=[('BACK', 'Backup'), ('TEST', 'Testing'), ('I.BS', 'Domain Error')], max_length=4, null=True),
        ),
    ]