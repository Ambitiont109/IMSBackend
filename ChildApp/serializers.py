from rest_framework import serializers
from .models import Child, AuthPerson, Contact, Picture, Food, MenuItem, InjureRecord, ChildDailyInformation, SiblingGroup
from drf_writable_nested.serializers import WritableNestedModelSerializer
from UserApp.models import User
from UserApp.serializers import UserSerializer
from anam_backend_main.myserializerfields import Base64ImageField
from anam_backend_main.constants import Parent
from django_seed import Seed


class SibilngChildSerializer(serializers.ModelSerializer):

    class Meta:
        model = Child
        fields = ['id', 'first_name', 'last_name', 'parent', 'photo']


class AuthPersonSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=False)

    class Meta:
        model = AuthPerson
        fields = '__all__'
        read_only_fields = ('child',)


class EmergencyContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = '__all__'
        read_only_fields = ('child',)


def generate_random_user():
    seeder = Seed.seeder()
    seeder.add_entity(User, 1)
    ret = seeder.execute()
    pk = ret[User][0]
    user = User.objects.filter(pk=pk).first()
    user.is_active = True
    user.is_superuser = False
    user.is_staff = False
    user.set_password('password')
    return user


class ChildSerializer(WritableNestedModelSerializer):
    siblings = serializers.SerializerMethodField(read_only=True)
    authPersons = AuthPersonSerializer(many=True)
    emergencyContacts = EmergencyContactSerializer(many=True)
    parent = UserSerializer(read_only=True)
    photo = Base64ImageField(required=False)

    class Meta:
        model = Child
        fields = '__all__'
        read_only_fields = ('sibling_group', )

    def get_siblings(self, obj):

        try:
            return SibilngChildSerializer(obj.sibling_group.childs.exclude(id=obj.id), many=True, context=self.context).data
        except Exception as e:
            return []

    def create(self, validated_data):
        user = self.context['request'].user
        sibling_group = None
        try:
            user_child = user.child
        except Exception:
            user_child = None
        if user_child:
            sibling_group = user.child.sibling_group
        if not sibling_group:
            sibling_group = SiblingGroup.objects.filter(
                numberOfSiblings=0).first()
        if not sibling_group:
            sibling_group = SiblingGroup.objects.create()
        # parent = user
        parent = generate_random_user()
        validated_data['sibling_group'] = sibling_group
        validated_data['parent'] = parent
        child = super(ChildSerializer, self).create(validated_data)

        parent.role = Parent
        parent.classnames = f'["{child.nameOfClass}"]'
        parent.save()

        child.sibling_group.numberOfSiblings += 1
        child.sibling_group.save()
        return child


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
        child_daily_info = ChildDailyInformation.objects.create(
            **validated_data)
        for injure_data in injures_data:
            InjureRecord.objects.create(
                dailyinfo=child_daily_info, **injure_data)
        return child_daily_info

    def update(self, instance, validated_data):
        injures_data = []
        if 'injures' in validated_data:
            injures_data = validated_data.pop('injures')
        injures = instance.injures.all()
        for index in range(0, len(injures)):
            if index < len(injures_data):
                serializer = InjureRecordSerializer(
                    instance=injures[index], data=injures_data[index])
                if serializer.is_valid():
                    serializer.save()
            if index >= len(injures_data):
                injures[index].delete()

        for index in range(0, len(injures_data) - len(injures)):
            InjureRecord.objects.create(
                dailyinfo=instance, **injures_data[index + len(injures)])

        child_daily_info = ChildDailyInformation.objects.create(
            **validated_data)
        for injure_data in injures_data:
            InjureRecord.objects.create(
                dailyinfo=child_daily_info, **injure_data)
        return child_daily_info


class ChildDailyInformationReadSerializer(serializers.ModelSerializer):
    injures = InjureRecordSerializer(many=True)
    menu = MenuItemSerializer(required=False)
    child = ChildSerializer()

    class Meta:
        model = ChildDailyInformation
        fields = '__all__'
