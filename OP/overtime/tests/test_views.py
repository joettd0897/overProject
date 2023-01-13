import datetime as dt

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import make_aware

from ..views import *
from ..models import *

class LoginTestCase(TestCase):
    def setUp(self) -> None:
        self.password ="password1234"
        self.user_01 = get_user_model().objects.create_user(
            username="user_01",
            email="a@a.com",
            password=self.password,
        )
        self.user_02 = get_user_model().objects.create_user(
            username="user_02",
            email="a@a.com",
            password=self.password,
        )
        self.u01_w01 = WorkModel.objects.create(
            name="u01_w01",
            hour_wage=1000,
            minute_wage=1000/60,
            user=self.user_01,
        )
        self.u02_w01 = WorkModel.objects.create(
            name="u02_w01",
            hour_wage=900,
            minute_wage=900/60,
            user=self.user_02,
        )
        self.u01_w01_o01 = OverTimeModel.objects.create(
            work=self.u01_w01,
            user=self.user_01,
            start_date=make_aware(timezone.datetime(2023, 1, 1, 10, 00)),
            end_date=make_aware(timezone.datetime(2023, 1, 1, 11, 00)),
            overtime_minute=60,
            overtime_wage=1250,
        )
        self.u02_w01_o01 = OverTimeModel.objects.create(
            work=self.u02_w01,
            user=self.user_02,
            start_date=make_aware(timezone.datetime(2023, 1, 1, 10, 00)),
            end_date=make_aware(timezone.datetime(2023, 1, 1, 11, 00)),
            overtime_minute=60,
            overtime_wage=1125,
        )

class TestOvertimeDelete(LoginTestCase, TestCase):
    def test_show_own_view(self):
        #自分のdeleteページにアクセス
        self.client.force_login(self.user_01)
        response = self.client.get(reverse("overtime:overtime_delete", args=[self.u01_w01_o01.pk]))
        self.assertEqual(response.status_code, 200)
    def test_dont_show_other_user(self):
        #他人のdeleteページにアクセス
        self.client.force_login(self.user_01)
        response = self.client.get(reverse("overtime:overtime_delete", args=[self.u02_w01_o01.pk]))
        self.assertEqual(response.status_code, 404)

class TestWorkDelete(LoginTestCase, TestCase):
    def test_show_own_view(self):
        #自分のdeleteページにアクセス
        self.client.force_login(self.user_01)
        response = self.client.get(reverse("overtime:work_delete", args=[self.u01_w01.pk]))
        self.assertEqual(response.status_code, 200)
    def test_dont_show_other_user(self):
        #他人のdeleteページにアクセス
        self.client.force_login(self.user_01)
        response = self.client.get(reverse("overtime:work_delete", args=[self.u02_w01.pk]))
        self.assertEqual(response.status_code, 404)

class TestOvertimeCalendar(LoginTestCase, TestCase):
    def test_show_own_view(self):
        #自分のページにアクセス
        self.client.force_login(self.user_01)
        response = self.client.get(reverse("overtime:overtime_calendar"))
        self.assertEqual(response.status_code, 200)
    def test_dont_show_other_user(self):
        #user01に2つuser02に1つのovertimeを設定
        u01_w01_o02 = OverTimeModel.objects.create(
            work=self.u01_w01,
            user=self.user_01,
            start_date=make_aware(timezone.datetime(2023, 1, 2, 10, 00)),
            end_date=make_aware(timezone.datetime(2023, 1, 2, 11, 00)),
            overtime_minute=60,
            overtime_wage=1250,
        )
        self.client.force_login(self.user_01)
        response = self.client.get(reverse("overtime:overtime_calendar"))
        #ページにアクセスしたときに自分のquerysetが返ってくることを確認
        query_len = len(response.context["object_list"])
        self.assertEqual(query_len, 2)

class TestWorkCreate(TestCase):
    def setUp(self) -> None:
        self.password ="password1234"
        self.user_01 = get_user_model().objects.create_user(
            username="user_01",
            email="a@a.com",
            password=self.password,
        )
    def test_work_access(self):
        #自分のページにアクセス
        self.client.force_login(self.user_01)
        response = self.client.get(reverse("overtime:work_register"))
        self.assertEqual(response.status_code, 200)

    def test_work_create(self):
        #作成をテスト
        self.client.force_login(self.user_01)
        data = {
            "name": "test01",
            "hour_wage": 60,
        }
        response = self.client.post(reverse("overtime:work_register"), data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        minute_wage = WorkModel.objects.values_list("minute_wage", flat=True).get(name="test01")
        self.assertEqual(minute_wage, 1.0)
        #ログインユーザーの情報でobjectが作成されたことを確認
        user = WorkModel.objects.values_list("user", flat=True).get(name="test01")
        self.assertEqual(user, self.user_01.pk)
        #objectの数を確認
        self.assertEqual(WorkModel.objects.all().count(), 1)

class TestOvertimeCreate(TestCase):
    def setUp(self) -> None:
        self.password ="password1234"
        self.user_01 = get_user_model().objects.create_user(
            username="user_01",
            email="a@a.com",
            password=self.password,
        )
        self.u01_w01 = WorkModel.objects.create(
            name="u01_w01",
            hour_wage=1000,
            minute_wage=1000 / 60,
            user=self.user_01,
        )
    def test_overtime_access(self):
        #アクセスを確認
        self.client.force_login(self.user_01)
        response = self.client.get(reverse("overtime:overtime_register"))
        self.assertEqual(response.status_code, 200)

    def test_overtime_create(self):
        #作成を確認
        self.client.force_login(self.user_01)
        data = {
            "work": self.u01_w01.pk,
            "start_date_0": "2023-01-01",
            "start_date_1": "10:00:00",
            "end_date_0": "2023-01-01",
            "end_date_1": "11:00:00",
            "break_time": 0,
        }
        response = self.client.post(reverse("overtime:overtime_register"), data=data, follow=True)
        #アクセスを確認
        self.assertEqual(response.status_code, 200)
        #作成されたことを確認
        self.assertEqual(OverTimeModel.objects.all().count(), 1)
    def test_overtime_create_time_is_wrong(self):
        data = {
            "work": self.u01_w01.pk,
            "start_date_0": "2023-01-02",
            "start_date_1": "10:00:00",
            "end_date_0": "2023-01-01",
            "end_date_1": "11:00:00",
            "break_time": 0,
        }
        response = self.client.post(reverse("overtime:overtime_register"), data=data, follow=True)
        self.assertEqual(OverTimeModel.objects.all().count(), 0)
        
