# Generated by Django 2.2.5 on 2019-12-06 10:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0020_auto_20191001_1235"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="machine",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="projects",
                to="main.Machine",
            ),
        ),
        migrations.AlterField(
            model_name="report",
            name="class_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("BACK", "Backup"),
                    ("TEST", "Testing"),
                    ("DEAD", "Deadline"),
                    ("MDEA", "Machine Deadline"),
                ],
                max_length=4,
                null=True,
                verbose_name="Type",
            ),
        ),
    ]
