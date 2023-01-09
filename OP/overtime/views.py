import json

from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import (TemplateView, CreateView, ListView,
                                  DeleteView, UpdateView,)
from .models import *
from .forms import *
from datetime import datetime
import datetime as dt
from decimal import Decimal, ROUND_HALF_UP

#暫定トップビュー
class TopView(LoginRequiredMixin, TemplateView):
    template_name = "overtime/top.html"

#仕事登録ビュー
class WorkCreateView(LoginRequiredMixin,CreateView):
    template_name = "overtime/work_create.html"
    model = WorkModel
    form_class = WorkCreateForm
    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.minute_wage = post.hour_wage / 60
        post.save()
        return redirect(reverse_lazy("overtime:work_list"))

#残業登録ビュー
class OvertimeCreateView(LoginRequiredMixin,CreateView):
    template_name = "overtime/overtime_create.html"
    model = OverTimeModel
    form_class = OverTimeCreateForm
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        #表示される仕事をリクエストユーザーに限定
        form.fields["work"].queryset = WorkModel.objects.filter(user=self.request.user)
        return form
    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        minute_wage = post.work.minute_wage
        overtime_minute = ((post.end_date - post.start_date).seconds - (post.break_time * 60)) // 60
        overtime_wage = Decimal(str(minute_wage * 1.25 * overtime_minute))
        post.overtime_wage = overtime_wage.quantize(Decimal("0"), rounding=ROUND_HALF_UP)
        post.overtime_minute = overtime_minute
        post.save()
        return redirect(reverse_lazy("overtime:overtime_calendar"))

class OvertimeListView(LoginRequiredMixin,ListView):
    template_name = "overtime/overtime_list.html"
    context_object_name = "object_list"
    model = OverTimeModel
    def get_queryset(self):
        queryset = OverTimeModel.objects.filter(user=self.request.user)
        self.form = form = OverTimeListForm(self.request.GET or None)

        if form.is_valid():
            year = form.cleaned_data.get("year")
            if year:
                queryset = OverTimeModel.objects.filter(start_date__year=year)

            month = form.cleaned_data.get("month")
            if month:
                queryset = OverTimeModel.objects.filter(start_date__month=month,
                                                        start_date__year=year)

        self.queryset = queryset
        return queryset
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context["search_form"] = self.form
        context["sum_wage"] = self.queryset.aggregate(Sum("overtime_wage"))["overtime_wage__sum"]
        context["sum_time"] = self.queryset.aggregate(Sum("overtime_minute"))["overtime_minute__sum"]
        return context

#残業をカレンダーとリストで表示
class OvertimeCalendarView(LoginRequiredMixin,ListView):
    template_name = "overtime/overtime_calendar.html"
    context_object_name = "object_list"
    model = OverTimeModel
    def get_queryset(self):
        #クエリをリクエストユーザーで絞り込み
        queryset = OverTimeModel.objects.filter(user=self.request.user)
        #formを取得しインスタンス変数化
        self.form = form = OvertimeCalendarForm(self.request.GET or None)

        if form.is_valid():
            year = form.cleaned_data.get("year")
            if year:
                queryset = OverTimeModel.objects.filter(start_date__year=year)

            month = form.cleaned_data.get("month")
            if month:
                queryset = OverTimeModel.objects.filter(start_date__month=month,
                                                        start_date__year=year).order_by("start_date")
        else:
            now = timezone.now()
            queryset = OverTimeModel.objects.filter(start_date__month=now.month,
                                                    start_date__year=now.year).order_by("start_date")

        self.queryset = queryset
        return queryset
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context["search_form"] = self.form
        context["sum_wage"] = self.queryset.aggregate(Sum("overtime_wage"))["overtime_wage__sum"]
        if self.queryset:
            sum_time = divmod(self.queryset.aggregate(Sum("overtime_minute"))["overtime_minute__sum"], 60)
            context["sum_hour"] = sum_time[0]
            context["sum_minute"] = str(sum_time[1]).zfill(2)
        #カレンダー用context
        event_array = []
        for event in self.queryset:
            tmp_array = {}
            tmp_array["title"] = str(format(event.overtime_wage, ",")) + "円"
            before_start = event.start_date + dt.timedelta(hours=9)
            before_end = event.end_date + dt.timedelta(hours=9)
            start_date = datetime.strptime(str(before_start.date()), "%Y-%m-%d").strftime("%Y-%m-%d")
            end_date = datetime.strptime(str(before_end.date()), "%Y-%m-%d").strftime("%Y-%m-%d")
            tmp_array["start"] = start_date
            tmp_array["end"] = end_date
            event_array.append(tmp_array)
        calendar_json = json.dumps(event_array)
        context["event_date"] = calendar_json
        year = self.request.GET.get("year")
        month = self.request.GET.get("month")
        if year and month:
            context["year"] = int(year)
            context["month"] = int(month) - 1
        else:
            context["year"] = datetime.now().year
            context["month"] = datetime.now().month - 1

        return context

class WorkListView(LoginRequiredMixin, ListView):
    model = WorkModel
    template_name = "overtime/work_list.html"
    context_object_name = "object_list"

class WorkUpdateView(LoginRequiredMixin, UpdateView):
    model = WorkModel
    form_class = WorkCreateForm
    template_name = "overtime/work_update.html"
    success_url = reverse_lazy("overtime:work_list")
    def get_object(self, queryset=None):
        model = super().get_object()
        if model.user != self.request.user:
            raise Http404
        else:
            return model
    def form_valid(self, form):
        post = form.save(commit=False)
        post.minute_wage = post.hour_wage / 60
        post.save()
        return redirect(reverse_lazy("overtime:work_list"))

'''
class OvertimeUpdateView(LoginRequiredMixin,UpdateView):
    model = OverTimeModel
    form_class = OverTimeCreateForm
    template_name = "overtime/overtime_update.html"
    success_url = reverse_lazy("overtime:top")
    def form_valid(self, form):
        post = form.save(commit=False)
        minute_wage = post.work.minute_wage
        overtime_minute = (post.end_date - post.start_date).seconds // 60
        overtime_wage = Decimal(str(minute_wage * 1.25 * overtime_minute))
        post.overtime_wage = overtime_wage.quantize(Decimal("0"), rounding=ROUND_HALF_UP)
        post.overtime_minute = overtime_minute
        post.save()
        return redirect(reverse_lazy("overtime:top"))
'''

class WorkDeleteView(LoginRequiredMixin,DeleteView):
    model = WorkModel
    template_name = "overtime/work_delete.html"
    success_url = reverse_lazy("overtime:work_list")
    def get_object(self, queryset=None):
        model = super().get_object()
        if model.user != self.request.user:
            raise Http404
        else:
            return model

class OvertimeDeleteView(LoginRequiredMixin,DeleteView):
    model = OverTimeModel
    template_name = "overtime/overtime_delete.html"
    success_url = reverse_lazy("overtime:overtime_calendar")
    def get_object(self, queryset=None):
        model = super().get_object()
        if model.user != self.request.user:
            raise Http404
        else:
            return model