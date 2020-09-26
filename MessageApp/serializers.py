from rest_framework import serializers
from .models import Message, AttachedFile
from UserApp.serializers import UserSerializer
from ChildApp.serializers import ChildSerializer


class AttachedFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = AttachedFile
        fields = '__all__'


class MessageReadSerializer(serializers.ModelSerializer):
    attachedFiles = AttachedFileSerializer(many=True)
    child = ChildSerializer()
    sender = UserSerializer()
    receiver = UserSerializer()

    class Meta:
        model = Message
        fields = '__all__'


class MessageWriteSerializer(serializers.ModelSerializer):
    # attachedFiles = serializers.PrimaryKeyRelatedField(many=True)
    # child = ChildSerializer()
    # sender = UserSerializer()
    # receiver = UserSerializer()

    class Meta:
        model = Message
        fields = '__all__'

    def create(self, validated_data):
        attachedFiles = []
        print(validated_data)
        if('attachedFiles' in validated_data):
            attachedFiles = validated_data.pop('attachedFiles')
        message = super().create(validated_data)
        for file in attachedFiles:
            try:
                message.attachedFiles.add(file)
            except Exception:
                pass
        return message

