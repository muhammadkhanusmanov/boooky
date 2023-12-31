from django.contrib import admin
from django.urls import path
from api.views import UserView, RegisterView,LogView,Logout, Avatarka,GetAvatar, MessageView, TestView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/',UserView.as_view()),
    path('signup/', RegisterView.as_view()),
    path('login/', LogView.as_view()),
    path('logout/', Logout.as_view()),
    path('addavatar/',Avatarka.as_view()),
    path('deleteavatar/',Avatarka.as_view()),
    path('uploadavatar/<str:id>',GetAvatar.as_view()),
    path('messages/',MessageView.as_view()),
    path('addmessage/',MessageView.as_view()),
    path('addtest/',TestView.as_view()),
    path('checktest/',TestView.as_view()),
]
