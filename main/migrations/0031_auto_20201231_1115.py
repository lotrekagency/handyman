# Generated by Django 2.2.13 on 2020-12-31 10:15

from django.db import migrations
import main.fields


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0030_auto_20191206_1643"),
    ]

    operations = [
        migrations.AlterField(
            model_name="frontendtest",
            name="assertion",
            field=main.fields.NonStrippingTextField(),
        ),
    ]
