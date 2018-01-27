# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-01-27 17:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deadline',
            name='dead_type',
            field=models.CharField(choices=[('DOM', 'Domain'), ('CERT', 'Certificate'), ('OTHR', 'Other')], default='OTHR', max_length=4),
        ),
    ]
