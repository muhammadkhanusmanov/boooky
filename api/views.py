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

from .models import User, Staff

from .serializers.user_serializers import UserSerializer, StaffSerializer

class UserView(APIView):
    def get(self, request):
        response = []
        users = User.objects.all()
        for user in users:
            staff = Staff.objects.get(user=user)
            staff = StaffSerializer(staff).data
            user = UserSerializer(user).data
            user['staff'] = staff
            response.append(user)
        return Response(response)

class RegisterView(APIView):
    '''sign up'''
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
                position = Staff.objects.create(user=user, staff='student')
                position.save()
                token = Token.objects.create(user=user)
                return Response({'status':True,'created user':str(user.staff),'token':token.key},status=status.HTTP_201_CREATED)
        return Response({'status':'BAD_REQUEST'},status=status.HTTP_400_BAD_REQUEST)

        