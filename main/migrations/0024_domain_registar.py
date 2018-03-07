# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-02 15:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_machine_name_on_reseller'),
    ]

    operations = [
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('panel_registar', models.CharField(blank=True, max_length=200, null=True)),
                ('username_panel_registar', models.CharField(blank=True, max_length=200, null=True)),
                ('password_panel_registar', models.CharField(blank=True, max_length=200, null=True)),
                ('registar', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Reseller')),
            ],
        ),
        migrations.CreateModel(
            name='Registar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
    ]