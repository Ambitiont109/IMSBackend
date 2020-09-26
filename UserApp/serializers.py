from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password

from .models import User
import json


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=50, validators=[UniqueValidator(queryset=User.objects.all())])
    classNames = serializers.SerializerMethodField()
    password = serializers.CharField(max_length=255, write_only=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'role', 'picture', 'classnames', 'classNames', 'password')

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
