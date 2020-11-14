from rest_framework import serializers
from .models import SchoolDocument, MiniClub, ExchangeLibrary, Marketing
from UserApp.serializers import UserSerializer
from UserApp.models import User
from ChildApp.models import Child
from ChildApp.serializers import SibilngChildSerializer


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
    children = SibilngChildSerializer(many=True, read_only=True)

    class Meta:
        model = MiniClub
        fields = '__all__'


class RegisterChildMiniClubSerializer(serializers.Serializer):
    child = serializers.PrimaryKeyRelatedField(queryset=Child.objects.all())


UnRegisterChildMiniClubSerializer = RegisterChildMiniClubSerializer


class ExchangeLibrarySerializer(serializers.ModelSerializer):
    child = SibilngChildSerializer(read_only=True)

    class Meta:
        model = ExchangeLibrary
        fields = '__all__'


class MarketingWriteSerializer(serializers.ModelSerializer):
    poster = serializers.PrimaryKeyRelatedField(queryset=User.objects.all,
                                                default=serializers.CurrentUserDefault())

    class Meta:
        model = Marketing
        fields = '__all__'


class MarketingReadSerializer(serializers.ModelSerializer):
    poster = UserSerializer()

    class Meta:
        model = Marketing
        fields = '__all__'
