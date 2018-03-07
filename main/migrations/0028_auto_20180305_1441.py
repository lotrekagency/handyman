# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-05 13:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_domain_end_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('end_time', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Certificateseller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('panel_seller', models.CharField(blank=True, max_length=200, null=True)),
                ('username_panel_seller', models.CharField(blank=True, max_length=200, null=True)),
                ('password_panel_seller', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='certificate',
            name='seller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Certificateseller'),
        ),
    ]