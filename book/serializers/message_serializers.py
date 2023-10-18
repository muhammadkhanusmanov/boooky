from rest_framework.serializers import ModelSerializer
from book.models import Message, Reply

class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class Replyserializer(ModelSerializer):
    class Meta:
        model =Reply
        fields = '__all__'