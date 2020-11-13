from django.shortcuts import render
from .serializers import NotificationStatusRecordSerializer, NotificationReadSerializer, NotificationWriteSerializer, NotificationReceiverSerializer
# from .models import Notification, NotificationStatusRecord
from rest_framework.decorators import action
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from anam_backend_main import mypermissions
# Create your views here.


class NotificationRecordListSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationStatusRecordSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filterset_fields = ['is_read']

    def get_queryset(self):
        user = self.request.user
        return user.received_notification_status.all()


class NotificationDataViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, mypermissions.IsAdminRole)

    def get_queryset(self):
        user = self.request.user
        return user.sent_notifications.order_by('-created_at').all()

    def get_serializer_class(self):
        user = self.request.user.id
        if 'sender' not in self.request.data:
            self.request.data['sender'] = user
        if self.action == 'list' or self.action == 'retrieve':
            return NotificationReadSerializer
        else:
            return NotificationWriteSerializer

    @action(detail=True, url_path='receivers')
    def getReceivers(self, request, pk=None):
        instance = self.get_object()
        serializer = NotificationReceiverSerializer(instance.notification_status_list.all(), many=True, context=self.get_serializer_context())
        return Response(serializer.data)
