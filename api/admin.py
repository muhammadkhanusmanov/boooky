from django.contrib import admin
from .models import Staff, Avatar, Message

admin.site.register(
    [Staff, Avatar, Message]
)
