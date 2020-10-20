from django.shortcuts import render
from .serializers import NotificationStatusRecordSerializer
# from .models import Notification, NotificationStatusRecord
from rest_framework import permissions, viewsets
# Create your views here.


class NotificationRecordListSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationStatusRecordSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filterset_fields = ['is_read']

    def get_queryset(self):
        user = self.request.user
        return user.received_notification_status.all()
