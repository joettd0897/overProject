# Generated by Django 4.1 on 2023-01-05 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("overtime", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="overtimemodel",
            name="break_time",
            field=models.PositiveSmallIntegerField(default=0, verbose_name="休憩時間"),
        ),
    ]
