from rest_framework import serializers
from .models import SchoolDocument


class UploadSerializer(serializers.Serializer):
    file = serializers.ImageField()


class SchoolDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = SchoolDocument
        fields = '__all__'


class SchoolDocumentUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = SchoolDocument
        fields = ['url', 'name', 'documentfor']
        read_only_fields = ['name', 'documentfor']
