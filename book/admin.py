from django.contrib import admin
from .models import Unversity_Ebook, Unversity_Pbooks, Students_book, UbookImage, SbookImage, Ebook, PositionUsers, Message,Reply

admin.site.register([
    Unversity_Ebook,
    Unversity_Pbooks,
    Students_book,
    UbookImage,
    SbookImage,
    Ebook,
    PositionUsers,
    Message,
    Reply
])