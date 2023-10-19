from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.http import HttpRequest,JsonResponse,FileResponse
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authentication import TokenAuthentication, BasicAuthentication

from .serializers.unversity_serializers import (
    EbookSerializer,PbookSerializer, UimageSerializer, BookfileSerializer, UserSerializer
)

from .serializers.message_serializers import (
    MessageSerializer, Replyserializer
)

from .serializers.student_serializers import SbookSerializer, SimageSerializer

from .models import (
    Unversity_Ebook,Students_book, SbookImage, UbookImage, Ebook, Unversity_Pbooks,PositionUsers,Message, Reply
)

class AdminView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]
    '''
    Add and delete a librarian
    '''
    def post(self, request):
        data = request.data
        username = data.get('username',None)
        password = data.get('password',None)
        first_name = data.get('first_name',username)
        if username is not None:
            try:
                user = User.objects.get(username=username)
                return Response({'Status':'This username is already'},status=status.HTTP_208_ALREADY_REPORTED)
            except:
                user = User.objects.create(
                    username=username,
                    password=make_password(password),
                    first_name=first_name
                )
                user.save()
                position = PositionUsers.objects.create(user=user, position='librarian')
                position.save()
                return Response({'Status':True},status=status.HTTP_201_CREATED)
        return Response({'Status':'BAD_REQUEST'},status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request):
        user_id = request.data
        user_id = user_id['user_id']
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return Response({'Status': True}, status=status.HTTP_200_OK)
        except:
            return Response({'Status': False}, status=status.HTTP_400_BAD_REQUEST)
    
class RegisterView(APIView):
    '''
    SignUp function
    '''
    def post(self, request):
        data = request.data
        username = data.get('username',None)
        password = data.get('password',None)
        first_name = data.get('first_name',username)
        if username is not None:
            try:
                user = User.objects.get(username=username)
                return Response({'status':'This username is already'},status=status.HTTP_208_ALREADY_REPORTED)
            except:
                user = User.objects.create(
                    username=username,
                    password=make_password(password),
                    first_name=first_name
                )
                user.save()
                position = PositionUsers.objects.create(user=user, position='student')
                position.save()
                token = Token.objects.create(user=user)
                return Response({'status':True,'staff':str(user.staff),'token':token.key},status=status.HTTP_201_CREATED)
        return Response({'status':'BAD_REQUEST'},status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    authentication_classes = [TokenAuthentication]
    '''
    User login
    '''
    def post(self, request):
        user = request.user
        token = Token.objects.get(user=user)
        return Response({'token':token.key,'staff':str(user.staff)})

class LogoutView(APIView):
    '''Logout'''
    authentication_classes = [TokenAuthentication]
    def delete(self, request):
        user = request.user
        token = Token.objects.get(user=user)
        token.delete()
        return Response({'status':True}, status=status.HTTP_200_OK)

class UserView(APIView):
    authentication_classes = [TokenAuthentication]
    '''
        get all users
    '''
    def get(self, request):
        user = request.user
        if str(user.staff)=='admin' or str(user.staff)=='librarian':
            users = User.objects.all()
            users = UserSerializer(users, many=True)
            return Response({'users': users.data}, status=status.HTTP_200_OK)
        return Response({'status':False}, status=status.HTTP_403_FORBIDDEN)
class EBookView(APIView):
    authentication_classes = [TokenAuthentication]
    '''
    add a new Ebook
    '''
    def post(self, request):
        user = request.user
        data = request.data
        staff = str(user.staff)
        if staff == 'admin' or staff == 'librarian':
            serialaizer = EbookSerializer(data=data)
            if serialaizer.is_valid():
                serialaizer.save()
                data = serialaizer.data
                return Response({'status': True,'id':data['id']},status=status.HTTP_201_CREATED)
            return Response({'status': False},status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': False},status=status.HTTP_403_FORBIDDEN)        
    
    '''add file for a ebook'''
    parser_classes = (MultiPartParser, FormParser)
    def put(self,request):
        user = request.user
        data = request.data
        staff = str(user.staff)
        if staff == 'admin' or  staff == 'librarian':
            serialazer = BookfileSerializer(data=data)
            if serialazer.is_valid():
                serialazer.save()
                book_file_id = serialazer.data['id']
                return Response({'status':True,'file_id':book_file_id},status=status.HTTP_201_CREATED)
            return Response({'status':False},status=status.HTTP_400_BAD_REQUEST)
        return Response({'status':False},status=status.HTTP_403_FORBIDDEN)
    
    '''delete a book by id'''
    def delete(self, request, id:int):
        user = request.user
        staff = str(user.staff)
        if staff == 'admin' or staff == 'librarian':
            try:
                book = Unversity_Ebook.objects.get(id=id)
                book.delete()
                return Response({'status': True}, status=status.HTTP_200_OK)
            except:
                return Response({'status': False}, status=status.HTTP_404_NOT_FOUND)
        return Response({'status': False}, status=status.HTTP_403_FORBIDDEN)

from telegram import Bot
class GetEbookView(APIView):
    '''get ebook by id'''
    def get(self,request,id:int):
        bot_token = "5976415526:AAHKVyCVeSb0_1xDRgLFz5zPLlhvwV9z_VM"  # O'zingizning botingizni tokeni bilan almashtiring
        bot = Bot(token=bot_token)
        chat_id = bot.get_chat()
        bot.send_message(chat_id=chat_id, text='hello')
        try:
            book =  Unversity_Ebook.objects.get(id=id)
            res1 =  EbookSerializer(book).data
            book_file = Ebook.objects.get(book=book)
            res2 = BookfileSerializer(book_file).data
            res = {'book':res1,'file':res2}
            return Response(res, status=status.HTTP_200_OK)
        except:
            return Response({'status':False}, status=status.HTTP_404_NOT_FOUND) 
    '''get all books'''
    def post(self,request):
        resp = []
        books = Unversity_Ebook.objects.all()
        for book in books:
            file = Ebook.objects.get(book=book)
            res1 = EbookSerializer(book).data
            res2 = BookfileSerializer(file).data
            resp.append({'book':res1, 'file':res2})
        return Response(resp, status=status.HTTP_200_OK)

class SavefileView(APIView):
    authentication_classes = [TokenAuthentication]
    def post(self, request,id:int):
        try:
            file = Ebook.objects.get(id=id)
            file = file.book_file
            print(file.path)
            file = open(file.path, 'rb')
            resp = FileResponse(file)
            return resp
        except:
            return Response({'status':False}, status=status.HTTP_400_BAD_REQUEST)

class GetImgView(APIView):
    def get(self, request,id:int):
        try:
            file = UbookImage.objects.get(id=id)
            file = file.image
            file = open(file.path, 'rb')
            resp = FileResponse(file)
            return resp
        except:
            return Response({'status':False}, status=status.HTTP_400_BAD_REQUEST)


class PBookView(APIView):
    '''add a new paper book'''
    authentication_classes = [TokenAuthentication]
    def post(self, request):
        user = request.user
        data = request.data
        staff = str(user.staff)
        if staff == 'admin' or staff == 'librarian':
            serializer = PbookSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                data = serializer.data
                return Response({'status':True,'book_id':data['id']}, status=status.HTTP_201_CREATED)
            return Response({'status':False},status=status.HTTP_400_BAD_REQUEST)
        return Response({'status':False},status=status.HTTP_403_FORBIDDEN)
    '''delete book'''
    def delete(self,request):
        user = request.user
        data = request.data
        staff = str(user.staff)
        if staff == 'admin' or staff == 'librarian':
            book = Unversity_Pbooks.objects.get(id=data['book_id'])
            book.delete()
            return Response({'status':True},status=status.HTTP_200_OK)
        return Response({'status':False},status=status.HTTP_403_FORBIDDEN)

class GetPBook(APIView):
    '''Get all pbooks'''
    def get(self,request):
        books = Unversity_Pbooks.objects.all()
        resp = []
        for book in books:
            img = UbookImage.objects.get(book=book)
            img = UimageSerializer(img).data
            book = PbookSerializer(book).data
            resp.append({'book':book, 'img':img})
            return Response(resp,status=status.HTTP_200_OK)
    '''Get a pbook by id'''
    def post(self,request):
        data = request.data
        book = Unversity_Pbooks.objects.get(id=data['id'])
        img = UbookImage.objects.get(book=book)
        res1 = PbookSerializer(book).data
        res2 = UimageSerializer(img).data
        resp = {'book': res1, 'img': res2}
        return Response(resp,status=status.HTTP_200_OK)
    '''search a pbook by title'''
    

class LibMessage(APIView):
    authentication_classes = [TokenAuthentication]
    '''get all messages'''
    def put(self,request):
        user = request.user
        staff = str(user.staff)
        if staff == 'librarian' or staff == 'admin':
            messages = Message.objects.all()
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({'status':False},status=status.HTTP_403_FORBIDDEN)

class UserMessage(APIView):
    authentication_classes = [TokenAuthentication]
    '''get user's messages'''
    def get(self,request):
        user = request.user
        try:
            messages = Message.objects.filter(user=user)
            serializer = MessageSerializer(messages, many=True)
            data = serializer.data
            return Response(data,status=status.HTTP_200_OK)
        except:
            return Response({'status':'Bildirishnomalar yo\'q'})
        
    '''Send a message to librarian for to get a book'''
    def post(self, request):
        user = request.user
        data = request.data
        serialazer = MessageSerializer(data=data)
        if serialazer.is_valid():
            serialazer.save()
            return Response({'status': True, 'message_id':serialazer.data['id']}, status=status.HTTP_200_OK)
        return Response({'status': False}, status=status.HTTP_400_BAD_REQUEST)
    
    '''get user's message by id'''
    def put(self,request,id:int):
        user = request.user
        try:
            msg = Message.objects.get(id=id)
            res1 = MessageSerializer(msg).data
            try:
                rpl = Reply.objects.get(message=msg)
                res2 = Replyserializer(rpl).data
            except:
                res2 = {}
        except:
            return Response({'status':False}, status=status.HTTP_404_NOT_FOUND)
        resp = {'message':res1, 'reply':res2}
        return Response(resp,status=status.HTTP_200_OK)

class ReplyView(APIView):
    authentication_classes = [TokenAuthentication]

    '''send a reply to a user'''
    def post(self,request):
        user = request.user
        data = request.data
        staff = str(user.staff)
        if staff=='admin' or staff=='librarian':
            serialazier = Replyserializer(data=data)
            if serialazier.is_valid():
                serialazier.save()
                return Response({'status': True, 'reply_id':serialazier.data['id']},status=status.HTTP_201_CREATED)
            return Response({'status':False},status=status.HTTP_403_FORBIDDEN)
        return Response({'status':False},status=status.HTTP_403_FORBIDDEN)

class SbookGet(APIView):
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        books = Students_book.objects.all()
        res = []
        for book in books:
            img = SbookImage.objects.get(book=book) 
            res1 = SbookSerializer(book).data
            res2 = SimageSerializer(img).data
            res.append({'book':res1, 'img':res2})
        return Response(res,status=status.HTTP_200_OK)
        
