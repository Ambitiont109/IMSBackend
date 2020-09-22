from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from .models import Child, AuthPerson, Contact
from UserApp.serializers import UserSerializer
import json


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
