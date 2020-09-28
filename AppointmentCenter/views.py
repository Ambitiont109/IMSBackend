from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from django.db.models import Q
from django.http import QueryDict
import json

from anam_backend_main import mypermissions
from .models import Appointment, TimeRangeItem, PresetItem, PresetRecord, PresetAppointment
from .models import PresetStatus
from UserApp.models import User
from .serializers import AppointmentWriteSerializer, AppointmentReadSerializer, PresetRecordSerializer,\
                         PresetAppointmentReadSerializer, PresetAppointmentWriteSerializer
from anam_backend_main.constants import Parent, Teacher, Admin, \
                                        Bamboo, Iroko, Baobab, Acajou
# Create your views here.


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentWriteSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if(self.request.user.role == Admin):
            return Appointment.objects.all()
        else:
            user = self.request.user
            return Appointment.objects.filter(Q(teacher=user) | Q(parent=user))

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve' or self.action == 'update':
            return AppointmentReadSerializer
        else:
            return AppointmentWriteSerializer

    @action(detail=False, url_path='user/(?P<userPk>\\d+)')
    def get_by_user(self, request, userPk=None):
        print("Hello World")
        user = get_object_or_404(User, pk=userPk)
        queryset = self.get_queryset().filter(Q(teacher=user) | Q(parent=user))
        serializer = AppointmentReadSerializer(queryset, many=True, context=self.get_serializer_context())
        return Response(serializer.data)


class PresetRecordViewSet(viewsets.ModelViewSet):
    queryset = PresetRecord.objects.all()
    serializer_class = PresetRecordSerializer
    permission_classes = (permissions.IsAuthenticated, mypermissions.IsAdminRole)

    @action(detail=False, url_path='current')
    def get_current_record(self, request, userPk=None):
        queryset = self.get_queryset().order_by('-created_at').first()
        if not queryset:
            return Response("There is not any record", status=status.HTTP_204_NO_CONTENT)
        serializer = PresetRecordSerializer(queryset, context=self.get_serializer_context())
        return Response(serializer.data)


class PresetAppointmentViewSet(viewsets.ModelViewSet):
    queryset = PresetAppointment.objects.all()
    permission_classes = (permissions.IsAuthenticated, )
    filterset_fields = ['className']

    def get_queryset(self):
        """
        current_preset=True in query parameter, return presetAppointments of current preset
        else; return All presetAppointments
        """
        req = self.request
        is_current_preset = req.query_params.get('current_preset')
        queryset = PresetAppointment.objects.none()
        if is_current_preset == 'true':

            currentRecord = PresetRecord.objects.filter(status=PresetStatus.Started).order_by('-created_at').first()
            if currentRecord:
                queryset = PresetAppointment.objects.filter(presetInfo=currentRecord)
            else:
                return PresetAppointment.objects.none()
        else:
            queryset = PresetAppointment.objects.all()
        if(self.request.user.role == Admin):
            return queryset
        else:
            user = self.request.user
            classnames = user.get_classnames()
            if len(classnames) == 0:
                return PresetAppointment.objects.none()
            q_object = Q()
            for name in classnames:
                q_object = q_object | Q(className=name)
            return PresetAppointment.objects.filter(q_object)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve' or self.action == 'update':
            return PresetAppointmentReadSerializer
        else:
            return PresetAppointmentWriteSerializer
