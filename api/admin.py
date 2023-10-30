from django.contrib import admin
from .models import Staff, Avatar

admin.site.register(
    [Staff, Avatar]
)
