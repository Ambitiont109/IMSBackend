from rest_framework import serializers
from .models import SchoolDocument, MiniClub, ExchangeLibrary


class UploadSerializer(serializers.Serializer):
    file = serializers.ImageField()


class SchoolDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = SchoolDocument
        fields = '__all__'


class SchoolDocumentUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = SchoolDocument
        fields = ['id', 'url', 'name', 'documentfor']
        read_only_fields = ['name', 'documentfor', 'id']


class MiniClubSerializer(serializers.ModelSerializer):

    class Meta:
        model = MiniClub
        fields = '__all__'


class ExchangeLibrarySerializer(serializers.ModelSerializer):

    class Meta:
        model = ExchangeLibrary
        fields = '__all__'
