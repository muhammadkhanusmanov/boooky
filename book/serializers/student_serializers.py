from rest_framework.serializers import ModelSerializer
from main_api.models import Students_book, SbookImage

class SbookSerializer(ModelSerializer):
    class Meta:
        model = Students_book
        fields = '__all__'

class SimageSerializer(ModelSerializer):
    class Meta:
        model = SbookImage
        fields = '__all__'