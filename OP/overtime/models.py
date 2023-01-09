import uuid

from django.db import models
from account.models import User
from django.utils import timezone


class WorkModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    user = models.ForeignKey(
        User,
        verbose_name="ユーザー",
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        verbose_name="仕事名",
        max_length=50,
    )
    hour_wage = models.PositiveSmallIntegerField(
        verbose_name="時給",
    )
    minute_wage = models.FloatField(
        verbose_name="分給",
    )
    def __str__(self):
        return self.name

class OverTimeModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    user = models.ForeignKey(
        User,
        verbose_name="ユーザー",
        on_delete=models.CASCADE,
    )
    work = models.ForeignKey(
        WorkModel,
        verbose_name="仕事名",
        on_delete=models.CASCADE,
    )
    start_date = models.DateTimeField(
        verbose_name="開始日時",
        default=timezone.now,
    )
    end_date = models.DateTimeField(
        verbose_name="終了日時",
        default=timezone.now,
    )
    overtime_minute = models.PositiveIntegerField(
        verbose_name="残業分数",
    )
    overtime_wage = models.PositiveIntegerField(
        verbose_name="残業代",
    )
    break_time = models.PositiveSmallIntegerField(
        verbose_name="休憩時間",
        default=0,
    )
    def __str__(self):
        return self.work.name

