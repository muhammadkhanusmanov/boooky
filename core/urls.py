from django.contrib import admin
from django.urls import path
from main_api.views import (
    AdminView,
    RegisterView,
    UserView,
    LoginView,SbookGet,SearchBooks,
    LogoutView,LibMessage,ReplyView,
    EBookView,PBookView,GetPBook,UserMessage,
    GetEbookView, SavefileView, GetImgView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add_librarian/', AdminView.as_view()),
    path('signin/', RegisterView.as_view()),
    path('all_users/', UserView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('addebook/',EBookView.as_view()),
    path('add_efile/', EBookView.as_view()),
    path('delete_ebook/<int:id>', EBookView.as_view()),
    path('get_ebook/<int:id>', GetEbookView.as_view()),
    path('get_ebooks/',GetEbookView.as_view()),
    path('save/<int:id>', SavefileView.as_view()),
    path('get_img/<int:id>', GetImgView.as_view()),
    path('addpbook/',PBookView.as_view()),
    path('delete_pbook/',PBookView.as_view()),
    path('getpbooks/',GetPBook.as_view()),
    path('getPbook/',GetPBook.as_view()),
    path('sendmessage/',UserMessage.as_view()),
    path('usermessages/',UserMessage.as_view()),
    path('allmessages/',LibMessage.as_view()),
    path('usermessage/<int:id>', UserMessage.as_view()),
    path('sendreply/',ReplyView.as_view()),
    path('getsbooks/',SbookGet.as_view()),
    path('sbook/<int:id>', SbookGet.as_view()),
    path('usersbooks/',SbookGet.as_view()),
    path('serchsbook/',SbookGet.as_view()),
    path('searchebook/',SearchBooks.as_view()),
    path('searchpbook/',SearchBooks.as_view()),
]
