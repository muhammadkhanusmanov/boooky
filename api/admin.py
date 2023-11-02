from django.contrib import admin
from .models import Staff, Avatar, Message,TestModel

admin.site.register(
    [Staff, Avatar, Message, TestModel]
)
