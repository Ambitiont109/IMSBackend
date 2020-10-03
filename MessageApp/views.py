from django.shortcuts import render
from django.db.models import Q
from rest_framework import viewsets, status, mixins
from rest_framework import permissions
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from .models import Message, AttachedFile
from .serializers import AttachedFileSerializer, MessageWriteSerializer, MessageReadSerializer, MessageComposeSerializer

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
        if self.request.user.role == Teacher:
            return Message.objects.filter(Q(sender=self.request.user) | Q(receiver=self.request.user))\
                .order_by('created_at')
        if self.request.user.role == Parent:
            children = self.request.user.child.sibling_group.childs.all()
            q_object = Q()
            for child in children:
                q_object = q_object | Q(child=child)
            print(q_object)
            return Message.objects.filter(q_object).order_by('created_at')

    @action(detail=False)
    def getHeaderMessages(self, request):
        queryset = self.get_queryset()

        headerMsgs = queryset.filter(
            headerMessage__isnull=True).order_by('-created_at').all()
        msgs = []
        for msg in headerMsgs:
            tempMsg = queryset.filter(
                headerMessage__id=msg.id).order_by('-created_at').first()
            if tempMsg:
                msgs.append(tempMsg)
            else:
                msgs.append(msg)
        serializer = MessageReadSerializer(
            msgs, many=True, context=self.get_serializer_context())
        return Response(serializer.data)

    @action(detail=True, url_path='linkedMessage')
    def getLinkedMesssage(self, request, pk=None):
        headerMessagePk = pk
        print(headerMessagePk)
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(headerMessage__id=headerMessagePk) | Q(
            pk=headerMessagePk)).order_by('created_at')
        serializer = MessageReadSerializer(
            queryset, many=True, context=self.get_serializer_context())
        return Response(serializer.data)


class AttachFileUploadView(generics.CreateAPIView):
    serializer_class = AttachedFileSerializer
    permission_classes = (permissions.IsAuthenticated, )


class MessageComposeView(generics.CreateAPIView):
    serializer_class = MessageComposeSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)
        children = self.request.user.child.sibling_group.childs.all()
        q_object = Q()
        for child in children:
            q_object = q_object | Q(child=child)
        queryset = Message.objects.filter(q_object)
        headerMsgs = queryset.filter(
            headerMessage__isnull=True).order_by('-created_at').all()
        msgs = []
        for msg in headerMsgs:
            tempMsg = queryset.filter(
                headerMessage__id=msg.id).order_by('-created_at').first()
            if tempMsg:
                msgs.append(tempMsg)
            else:
                msgs.append(msg)
        serializer = MessageReadSerializer(
            msgs, many=True, context=self.get_serializer_context())
        return Response(serializer.data)


class MessageReplyView(generics.CreateAPIView):
    serializer_class = MessageComposeSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, headerpk=None,*args, **kwargs):
        self.create(request, *args, **kwargs)
        queryset = Message.objects.all()
        queryset = queryset.filter(Q(headerMessage__id=headerpk) | Q(
            pk=headerpk)).order_by('created_at')
        serializer = MessageReadSerializer(
            queryset, many=True, context=self.get_serializer_context())
        return Response(serializer.data)
