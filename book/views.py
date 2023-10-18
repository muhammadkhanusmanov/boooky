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