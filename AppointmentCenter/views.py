from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
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
    PresetAppointmentReadSerializer, PresetAppointmentWriteSerializer, PresetItemSerializer, TimeRangeSerializer
from anam_backend_main.constants import Parent, Teacher, Admin, \
    Bamboo, Iroko, Baobab, Acajou
# Create your views here.


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentWriteSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if(self.request.user.role == Admin):
            return Appointment.objects.all()
        elif self.request.user.role == Teacher:
            return Appointment.objects.filter(teacher=user)
        else:
            queryset = user.child.sibling_group.childs.all()
            return Appointment.objects.filter(child__in=queryset)

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
        serializer = AppointmentReadSerializer(
            queryset, many=True, context=self.get_serializer_context())
        return Response(serializer.data)


class PresetRecordViewSet(viewsets.ModelViewSet):
    queryset = PresetRecord.objects.all()
    serializer_class = PresetRecordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @action(detail=False, url_path='current')
    def get_current_record(self, request, userPk=None):
        queryset = self.get_queryset().order_by('-created_at').first()
        if not queryset:
            return Response("There is not any record", status=status.HTTP_204_NO_CONTENT)
        serializer = PresetRecordSerializer(
            queryset, context=self.get_serializer_context())
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        validated_data = request.data
        if('presetItems' in validated_data):
            presetItemsData = validated_data.pop('presetItems')

            for presetItemData in presetItemsData:
                presetItem = get_object_or_404(
                    PresetItem, pk=presetItemData.get('id'))

                if 'timeranges' in presetItemData:
                    timeranges_data = presetItemData.pop('timeranges')
                    id_list = []
                    for timerange_data in timeranges_data:
                        pk = timerange_data.pop('id')
                        timerangeItem = None
                        created = False
                        try:
                            timerangeItem = TimeRangeItem.objects.get(
                                pk=pk, presetItem=presetItem)
                        except ObjectDoesNotExist:
                            timerangeItem = TimeRangeItem.objects.create(
                                presetItem=presetItem, **timerange_data)
                            timerangeItem.save()
                        id_list.append(timerangeItem.id)
                        if not created:
                            timerangeSerializer = TimeRangeSerializer(
                                instance=timerangeItem, data=timerange_data, partial=partial)
                            if timerangeSerializer.is_valid():
                                timerangeSerializer.save()
                            else:
                                return Response(timerangeSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    timeranges = presetItem.timeranges.all()
                    for timerange in timeranges:
                        if timerange.id not in id_list:
                            timerange.delete()
                print(presetItem)
                presetItemSerializer = PresetItemSerializer(
                    instance=presetItem, data=presetItemData, partial=partial)
                if presetItemSerializer.is_valid():
                    presetItemSerializer.save()
                else:
                    return Response(presetItemSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

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
        print(is_current_preset)
        if is_current_preset == 'true':

            currentRecord = PresetRecord.objects.filter(
                status=PresetStatus.Started).order_by('-created_at').first()
            if currentRecord:
                queryset = PresetAppointment.objects.filter(
                    presetInfo=currentRecord)
            else:
                return PresetAppointment.objects.none()
        else:
            queryset = PresetAppointment.objects.all()
        if(self.request.user.role == Admin):
            return queryset
        elif self.request.user.role == Teacher:
            user = self.request.user
            classnames = user.get_classNames()
            if len(classnames) == 0:
                return PresetAppointment.objects.none()
            q_object = Q()
            for name in classnames:
                q_object = q_object | Q(className=name)
            print( PresetAppointment.objects.filter(q_object))
            return PresetAppointment.objects.filter(q_object)
        else:
            return queryset

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve' or self.action == 'update':
            return PresetAppointmentReadSerializer
        else:
            return PresetAppointmentWriteSerializer

    @action(detail=False, url_path='current_user')
    def get_preset_apnts_current_user(self, request):
        user = request.user
        if user.role != Parent:
            return Response([])
        children = user.child.sibling_group.childs.all()
        serializer = PresetAppointmentReadSerializer(PresetAppointment.objects.filter(child__in=children).all(), many=True,
                                                     context=self.get_serializer_context())
        return Response(serializer.data)
