from rest_framework.serializers import ModelSerializer, StringRelatedField
from django.contrib.auth.models import User
from main_api.models import Unversity_Pbooks, Unversity_Ebook, UbookImage, Ebook

class PbookSerializer(ModelSerializer):
    class Meta:
        model = Unversity_Pbooks
        fields = '__all__'

class EbookSerializer(ModelSerializer):
    class Meta:
        model = Unversity_Ebook
        fields = '__all__'
class UimageSerializer(ModelSerializer):
    class Meta:
        model = UbookImage
        fields = '__all__'

class BookfileSerializer(ModelSerializer):
    class Meta:
        model = Ebook
        fields = '__all__'
class UserSerializer(ModelSerializer):
    staff = StringRelatedField()
    class Meta:
        model = User
        fields = ['id','username', 'first_name','staff']