from django.urls import path
from .views import *

app_name = "overtime"

urlpatterns = [
    path("", TopView.as_view(), name="top"),
    path("work/register/", WorkCreateView.as_view(), name="work_register"),
    path("work/list/", WorkListView.as_view(), name="work_list"),
    path("work/<uuid:pk>/update/", WorkUpdateView.as_view(), name="work_update"),
    path("work/<uuid:pk>/delete/", WorkDeleteView.as_view(), name="work_delete"),
    path("overtime/register/", OvertimeCreateView.as_view(), name="overtime_register"),
    #path("overtime/list/", OvertimeListView.as_view(), name="overtime_list"),
    path("overtime/calendar/", OvertimeCalendarView.as_view(), name="overtime_calendar"),
    #path("overtime/<uuid:pk>/update/", OvertimeUpdateView.as_view(), name="overtime_update"),
    path("overtime/<uuid:pk>/delete/", OvertimeDeleteView.as_view(), name="overtime_delete"),
]