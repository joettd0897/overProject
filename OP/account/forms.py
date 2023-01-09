from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

CustomUser = get_user_model()

class UserCreateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [CustomUser.USERNAME_FIELD] + CustomUser.REQUIRED_FIELDS + ["password1", "password2"]


class LoginForm(AuthenticationForm):
    pass