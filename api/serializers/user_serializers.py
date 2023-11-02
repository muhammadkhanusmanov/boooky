from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from ..models import (
    Staff, Avatar, Message, TestModel
)

class StaffSerializer(ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email','staf','pic')

class AvatarSerializer(ModelSerializer):
    class Meta:
        model = Avatar
        fields = '__all__'

class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class TestSerializer(ModelSerializer):
    class Meta:
        model = TestModel
        fields = '__all__'
        
