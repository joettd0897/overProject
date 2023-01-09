from django.contrib import admin
from .models import *
from account.models import User

admin.site.register(WorkModel)
admin.site.register(OverTimeModel)
admin.site.register(User)
