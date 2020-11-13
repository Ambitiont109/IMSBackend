from rest_framework import serializers
from .models import Notification, NotificationStatusRecord
from UserApp.serializers import UserSerializer
from UserApp.models import User
from ChildApp.models import Child
from . import utils
from anam_backend_main.constants import Teacher, Parent
class NotificationReadSerializer(serializers.ModelSerializer):
    sender = UserSerializer()

    class Meta:
        model = Notification
        fields = '__all__'


class NotificationWriteSerializer(serializers.ModelSerializer):
    receivers = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())


    class Meta:
        model = Notification
        fields = '__all__'

    def create(self, validated_data):
        receivers = validated_data.pop('receivers')
        instance = super().create(validated_data)
        if instance.is_child_broadcast:
            for child in Child.objects.all():
                receiver = child.parent
                NotificationStatusRecord.objects.create(notification=instance, receiver=receiver, is_read=False)
                utils.create_notification_record(receiver, instance)
        if instance.is_teacher_broadcast:
            for receiver in User.objects.filter(role=Teacher).all():
                NotificationStatusRecord.objects.create(notification=instance, receiver=receiver, is_read=False)
                utils.create_notification_record(receiver, instance)
        print(validated_data)
        for receiver in receivers:
            if instance.is_child_broadcast and receiver.role == Parent:
                continue
            if instance.is_teacher_broadcast and receiver.role == Teacher:
                continue
            NotificationStatusRecord.objects.create(notification=instance, receiver=receiver, is_read=False)
            utils.create_notification_record(receiver, instance)
        return instance


class NotificationStatusRecordSerializer(serializers.ModelSerializer):
    notification = NotificationReadSerializer()

    class Meta:
        model = NotificationStatusRecord
        fields = '__all__'
        read_only_fields = ('notification', )


class NotificationReceiverSerializer(serializers.ModelSerializer):
    receiver = UserSerializer()

    class Meta:
        model = NotificationStatusRecord
        fields = ('receiver', 'is_read', 'id')
