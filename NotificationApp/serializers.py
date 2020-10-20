from rest_framework import serializers
from .models import Notification, NotificationStatusRecord
from UserApp.serializers import UserSerializer


class NotificationSerializer(serializers.ModelSerializer):
    sender = UserSerializer()

    class Meta:
        model = Notification
        fields = '__all__'


class NotificationStatusRecordSerializer(serializers.ModelSerializer):
    notification = NotificationSerializer()

    class Meta:
        model = NotificationStatusRecord
        fields = '__all__'
        read_only_fields = ('notification', )
