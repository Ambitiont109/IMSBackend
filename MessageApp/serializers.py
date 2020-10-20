from rest_framework import serializers
from .models import Message, AttachedFile
from UserApp.models import User
from ChildApp.models import Child
from UserApp.serializers import UserSerializer
from ChildApp.serializers import ChildSerializer
from anam_backend_main.myserializerfields import Base64ImageField
from NotificationApp import utils as notfication_utils

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

def resolveHeaderLastMessage(msg):
    if msg.headerMessage:
        msg.headerMessage.lastMessage = msg
    else:
        msg.lastMessage = msg
    msg.save()

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
        resolveHeaderLastMessage(message)
        notfication_utils.message_create_notification(message)
        for file in attachedFiles:
            try:
                message.attachedFiles.add(file)
            except Exception:
                pass
        
        return message


class MessageComposeImageSerializer(serializers.ModelSerializer):
    file = Base64ImageField()

    class Meta:
        model = AttachedFile
        fields = ('file', )


class MessageComposeSerializer(serializers.ModelSerializer):
    attachedFiles = MessageComposeImageSerializer(many=True)
    receivers = serializers.ListField(child=serializers.PrimaryKeyRelatedField(queryset=User.objects.all()), write_only=True)
    # content = serializers.CharField()
    # subject = serializers.CharField()
    # child = serializers.PrimaryKeyRelatedField(queryset=Child.objects.all())
    # sender = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ('content', 'subject', 'attachedFiles', 'child', 'receivers', 'sender', 'msgType', 'headerMessage')


    def create(self, validated_data):
        attachedFiles = validated_data.pop('attachedFiles')
        fileList = []
        for file in attachedFiles:
            serializer = MessageComposeImageSerializer(data=file)
            if serializer.is_valid():
                fileList.append(serializer.save())
                print(serializer.data)
            else:
                print(serializer.errors)
        receivers = validated_data.pop('receivers')
        msg = Message.objects.first()
        for receiver in receivers:
            msg = Message.objects.create(**validated_data, receiver=receiver)
            msg.attachedFiles.set(fileList)
            msg.save()
            resolveHeaderLastMessage(msg)
            notfication_utils.message_create_notification(msg)
        return msg

