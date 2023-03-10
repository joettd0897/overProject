from django import forms
from django.utils import timezone
from .models import *
import datetime as dt

class WorkCreateForm(forms.ModelForm):
    class Meta:
        model = WorkModel
        fields = [
            "name",
            "hour_wage",
        ]

class OverTimeCreateForm(forms.ModelForm):
    now = dt.datetime.now()
    now_str = now.strftime('%Y%m%d%H%M')
    now_dt = dt.datetime.strptime(now_str, '%Y%m%d%H%M')
    start_date = forms.SplitDateTimeField(label="開始時間",
                                          widget=forms.SplitDateTimeWidget(date_attrs={"type": "date",},
                                                                           time_attrs={"type": "time"}),
                                          initial=now_dt)
    end_date = forms.SplitDateTimeField(label="終了時間",
                                        widget=forms.SplitDateTimeWidget(date_attrs={"type": "date"},
                                                                         time_attrs={"type": "time"}),
                                        initial=now_dt)
    def __init__(self, *args, **kwargs):
        super(OverTimeCreateForm, self).__init__(*args, **kwargs)
    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_date")
        end = cleaned_data.get("end_date")
        if end < start:
            raise forms.ValidationError('時間がおかしいです。', code="time_is_wrong")

        break_time = cleaned_data.get("break_time")
        overtime = (end - start).seconds // 60
        if break_time >= overtime:
            raise forms.ValidationError("休憩時間がおかしいです。", code="break_is_wrong")
    class Meta:
        model = OverTimeModel
        fields = [
            "work",
            "start_date",
            "end_date",
            "break_time",
        ]

class OverTimeListForm(forms.Form):
    start_year = 2022
    end_year = timezone.now().year + 1
    year_list = [(year, year) for year in reversed(range(start_year, end_year))]
    YEAR_CHOICE = tuple(year_list)
    year = forms.ChoiceField(
        label="年",
        required=True,
        choices=YEAR_CHOICE,
    )

    month_list = [(month, month) for month in range(1, 13)]
    month_list.insert(0,("", ""))
    MONTH_CHOICE = tuple(month_list)
    month = forms.ChoiceField(
        label="月",
        required=False,
        choices=MONTH_CHOICE,
    )

class OvertimeCalendarForm(forms.Form):
    start_year = 2022
    end_year = timezone.now().year + 1
    year_list = [(year, year) for year in reversed(range(start_year, end_year))]
    YEAR_CHOICE = tuple(year_list)
    year = forms.ChoiceField(
        label="年",
        required=True,
        choices=YEAR_CHOICE,
    )

    month_list = [(month, month) for month in range(1, 13)]
    MONTH_CHOICE = tuple(month_list)
    month = forms.ChoiceField(
        label="月",
        required=False,
        choices=MONTH_CHOICE,
    )
