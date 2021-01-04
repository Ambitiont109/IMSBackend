from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password
from .models import User
from ChildApp.models import Child
import json


class ChildSmallSerializer(serializers.ModelSerializer):

    class Meta:
        model = Child
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=50, validators=[UniqueValidator(queryset=User.objects.all())])
    classNames = serializers.SerializerMethodField()
    password = serializers.CharField(max_length=255, write_only=True, required=False)
    child = ChildSmallSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'role', 'phoneNumber', 'address',
                  'picture', 'classnames', 'classNames', 'password', 'child')

    def get_classNames(self, obj):
        try:
            data = json.loads(obj.classnames)
            if(type(data) == type([])):
                return data
            return []
        except Exception:
            return []

    def create(self, validated_data):
        print(validated_data)
        if 'password' in validated_data:
            print(True)
            validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)


class PasswordSerializer(serializers.Serializer):
    current_pwd = serializers.CharField(required=True)
    new_pwd = serializers.CharField(required=True)


class PasswordSerializerTwo(serializers.Serializer):
    new_pwd = serializers.CharField(required=True)
