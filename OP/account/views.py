from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (CreateView,)
from django.contrib.auth.views import LoginView, LogoutView
from .forms import *

class UserCreateView(CreateView):
    template_name = "account/user_create.html"
    form_class = UserCreateForm
    success_url = reverse_lazy("overtime:top")

class LoginView(LoginView):
    template_name = "account/login.html"
    form_class = LoginForm

class LogoutView(LogoutView):
    template_name = "account/logout.html"