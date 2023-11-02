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

from .models import User, Staff, Avatar, Message

from .serializers.user_serializers import UserSerializer, StaffSerializer, AvatarSerializer, MessageSerializer

class UserView(APIView):
    def get(self, request):
        response = []
        users = User.objects.all()
        a=0
        for user in users:
            staff = Staff.objects.get(user=user)
            staff = str(staff.staff)
            user = UserSerializer(user).data
            user['staff'] = staff
            try:
                user['img'] = f'https://boookyuz.pythonanywhere.com/uploadavatar/{user["pic"][0]}'
                response.append(user)
            except:
                response.append(user)
        return Response(response)

class RegisterView(APIView):
    '''sign up'''
    def post(self, request):
        print(1)
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
                position = Staff.objects.create(user=user, staff='student')
                position.save()
                token = Token.objects.create(user=user)
                return Response({'status':True,'staff':str(position.staff),'token':token.key},status=status.HTTP_201_CREATED)
        return Response({'status':'BAD_REQUEST'},status=status.HTTP_400_BAD_REQUEST)

class LogView(APIView):
    authentication_classes = [BasicAuthentication]
    def post(self, request):
        user = request.user
        token = Token.objects.get_or_create(user=user)
        token = str(token[0])
        staff = Staff.objects.get(user=user)
        return Response({'token':token,'staff':str(staff.staff)})

class Logout(APIView):
    '''logout user'''
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def delete(self,request):
        user = request.user
        token = Token.objects.get(user=user)
        token.delete()
        return Response({'status':'Token deleted'},status=status.HTTP_200_OK)

class Avatarka(APIView):
    '''Add a image for a user'''
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request):
        user = request.user
        image = request.data.get('img', None)
        if image is not None:
            avatar = Avatar.objects.create(
                user=user,
                img=image
            )
            avatar.save()
            return Response({'status': 'Avatar yaratildi','user': str(user.username)},status=status.HTTP_201_CREATED)
        return Response({'status': 'Image topilmadi'},status=status.HTTP_400_BAD_REQUEST)

    '''delete image'''
    def delete(self, request):
        user = request.user
        try:
            img = Avatar.objects.get(user=user)
            img.delete()
            return Response({'status':'Avatar o\'chirildi', 'username':str(user.username)}, status=status.HTTP_200_OK)
        except:
            return Response({'status':'Avatar yo\'q', 'username':str(user.username)}, status=status.HTTP_400_BAD_REQUEST)
    
class GetAvatar(APIView):
    def get(self, request,id:str):
        try:
            file = Avatar.objects.get(id=id)
            img =file.img 
            file = open(img.path, 'rb')
            resp = FileResponse(img)
            return resp
        except:
            return Response({'status':False}, status=status.HTTP_400_BAD_REQUEST)
    

class MessageView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        user = request.user
        result = {'user':str(user.id),'messages':[]}
        messages = Message.objects.all()
        for message in messages:
            msg = MessageSerializer(message).data
            result['messages'].append(msg)
        return Response(result, status=status.HTTP_200_OK)
    def put(self,request):
        user = request.user
        data = request.data
        try:
            msg = Message.objects.create(
                from_user=user,
                text=data['text']
            )
            msg.save()
            msg = MessageSerializer(msg).data
            return Response({'status':True,'message':msg}, status.HTTP_200_OK)
        except:
            return Response({'status':False}, status.HTTP_400_BAD_REQUEST)
    