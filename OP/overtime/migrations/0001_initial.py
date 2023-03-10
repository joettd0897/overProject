# Generated by Django 4.1 on 2023-01-03 23:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="WorkModel",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="仕事名")),
                ("hour_wage", models.PositiveSmallIntegerField(verbose_name="時給")),
                ("minute_wage", models.FloatField(verbose_name="分給")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="ユーザー",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OverTimeModel",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "start_date",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="開始日時"
                    ),
                ),
                (
                    "end_date",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="終了日時"
                    ),
                ),
                ("overtime_minute", models.PositiveIntegerField(verbose_name="残業分数")),
                ("overtime_wage", models.PositiveIntegerField(verbose_name="残業代")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="ユーザー",
                    ),
                ),
                (
                    "work",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="overtime.workmodel",
                        verbose_name="仕事名",
                    ),
                ),
            ],
        ),
    ]
