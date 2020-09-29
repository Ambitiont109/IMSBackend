from rest_framework import serializers
from .models import Child, AuthPerson, Contact, Picture, Food, MenuItem, InjureRecord, ChildDailyInformation
from UserApp.serializers import UserSerializer


class SibilngChildSerializer(serializers.ModelSerializer):

    class Meta:
        model = Child
        fields = ['id', 'first_name', 'last_name', 'parent', 'photo']


class AuthPersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuthPerson
        fields = '__all__'


class EmergencyContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = '__all__'


class ChildSerializer(serializers.ModelSerializer):
    siblings = serializers.SerializerMethodField()
    authPersons = AuthPersonSerializer(many=True)
    emergenyContacts = EmergencyContactSerializer(many=True)
    parent = UserSerializer()

    class Meta:
        model = Child
        fields = '__all__'

    def get_siblings(self, obj):

        try:
            return SibilngChildSerializer(obj.sibling_group.childs.exclude(id=obj.id), many=True, context=self.context).data
        except Exception as e:
            return []
    # def create(self, validated_data):
    #     print(validated_data)
    #     if 'password' in validated_data:
    #         print(True)
    #         validated_data['password'] = make_password(validated_data.get('password'))
    #     return super(ChildSerializer, self).create(validated_data)


class PictureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Picture
        fields = '__all__'
        read_only_fields = ('receiver', )


class FoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Food
        fields = '__all__'


class MenuItemSerializer(serializers.ModelSerializer):

    foods = FoodSerializer(many=True, read_only=True)

    class Meta:
        model = MenuItem
        fields = '__all__'


class AddFoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = MenuItem
        fields = '__all__'


class InjureRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = InjureRecord
        fields = '__all__'
        read_only_fields = ('dailyinfo', )




class ChildDailyInformationWriteSerializer(serializers.ModelSerializer):
    injures = InjureRecordSerializer(many=True)


    class Meta:
        model = ChildDailyInformation
        fields = '__all__'

    def create(self, validated_data):
        injures_data = validated_data.pop('injures')
        child_daily_info = ChildDailyInformation.objects.create(**validated_data)
        for injure_data in injures_data:
            InjureRecord.objects.create(dailyinfo=child_daily_info, **injure_data)
        return child_daily_info

    def update(self, instance, validated_data):
        injures_data = validated_data.pop('injures')
        injures = instance.injures.all()
        for index in range(0, len(injures)):
            if index < len(injures_data):
                serializer = InjureRecordSerializer(instance=injures[index], data=injures_data[index])
                if serializer.is_valid():
                    serializer.save()
            if index >= len(injures_data):
                injures[index].delete()

        for index in range(0, len(injures_data) - len(injures)):
            InjureRecord.objects.create(dailyinfo=instance, **injures_data[index + len(injures)])

        child_daily_info = ChildDailyInformation.objects.create(**validated_data)
        for injure_data in injures_data:
            InjureRecord.objects.create(dailyinfo=child_daily_info, **injure_data)
        return child_daily_info


class ChildDailyInformationReadSerializer(serializers.ModelSerializer):
    injures = InjureRecordSerializer(many=True)
    menu = MenuItemSerializer(required=False)
    child = ChildSerializer()

    class Meta:
        model = ChildDailyInformation
        fields = '__all__'
