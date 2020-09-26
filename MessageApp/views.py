from django.shortcuts import render
from django.db.models import Q
from rest_framework import viewsets, status, mixins
from rest_framework import permissions
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from .models import Message, AttachedFile
from .serializers import AttachedFileSerializer, MessageWriteSerializer, MessageReadSerializer

from anam_backend_main.constants import Admin, Teacher, Parent
# Create your views here.


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageWriteSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve' or self.action == 'update':
            return MessageReadSerializer
        else:
            return MessageWriteSerializer

    def get_queryset(self):
        if self.request.user.role == Admin:
            return Message.objects.filter(Q(sender__role=Admin) | Q(receiver__role=Admin)).order_by('created_at')
        return Message.objects.filter(Q(sender=self.request.user) | Q(receiver=self.request.user))\
            .order_by('created_at')


    @action(detail=False)
    def getHeaderMessages(self, request):
        queryset = self.get_queryset()
        headerMsgs = queryset.filter(headerMessage__isnull=True).order_by('-created_at').all()
        msgs = []
        for msg in headerMsgs:
            tempMsg = queryset.filter(headerMessage__id=msg.id).order_by('-created_at').first()
            if tempMsg:
                msgs.append(tempMsg)
            else:
                msgs.append(msg)
        serializer = MessageReadSerializer(msgs, many=True, context=self.get_serializer_context())
        return Response(serializer.data)

    @action(detail=True, url_path='linkedMessage')
    def getLinkedMesssage(self, request, pk=None):
        headerMessagePk = pk
        print(headerMessagePk)
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(headerMessage__id=headerMessagePk) | Q(pk=headerMessagePk)).order_by('created_at')
        serializer = MessageReadSerializer(queryset, many=True, context=self.get_serializer_context())
        return Response(serializer.data)


class AttachFileUploadView(generics.CreateAPIView):
    serializer_class = AttachedFileSerializer
    permission_classes = (permissions.IsAuthenticated, )
