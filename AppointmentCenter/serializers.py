from rest_framework import serializers
from .models import Appointment, TimeRangeItem, PresetItem, PresetRecord, PresetAppointment
from UserApp.serializers import UserSerializer
from ChildApp.serializers import ChildSerializer


class AppointmentWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = '__all__'


class AppointmentReadSerializer(serializers.ModelSerializer):
    child = ChildSerializer()
    teacher = UserSerializer()
    parent = UserSerializer()

    class Meta:
        model = Appointment
        fields = '__all__'


class TimeRangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimeRangeItem
        fields = '__all__'



class PresetItemSerializer(serializers.ModelSerializer):
    timeranges = TimeRangeSerializer(many=True)

    class Meta:
        model = PresetItem
        exclude = ('presetRecord', )



class PresetRecordSerializer(serializers.ModelSerializer):
    presetItems = PresetItemSerializer(many=True)

    class Meta:
        model = PresetRecord
        fields = '__all__'

    def create(self, validated_data):
        presetItemsData = validated_data.pop('presetItems')
        presetRecord = PresetRecord.objects.create(**validated_data)
        for presetItemData in presetItemsData:
            timeranges_data = presetItemData.pop('timeranges')
            preset_item = PresetItem.objects.create(presetRecord=presetRecord, **presetItemData)
            for timerange_data in timeranges_data:
                TimeRangeItem.objects.create(presetItem=preset_item, **timerange_data)
        return presetRecord

    # def update(self, instance, validated_data):
    #     if('presetItems' in validated_data):
    #         presetItemsData = validated_data.pop('presetItems')
    #         for presetItemData in presetItemsData:
    #             print(type(presetItemData))
    #             print(presetItemData['duration'])
    #             if 'timeranges' in presetItemData:
    #                 timeranges_data = presetItemData.pop('timeranges')
    #                 for timerange_data in timeranges_data:
    #                     print(timerange_data)
    #     return super().update(instance, validated_data)


class PresetAppointmentReadSerializer(serializers.ModelSerializer):
    timerange = TimeRangeSerializer()
    child = ChildSerializer()

    class Meta:
        model = PresetAppointment
        fields = '__all__'


class PresetAppointmentWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = PresetAppointment
        fields = '__all__'
