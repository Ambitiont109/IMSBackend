from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ObjectDoesNotExist
from .models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=50, validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'role', 'picture', 'classnames')


class PasswordSerializer(serializers.Serializer):
    current_pwd = serializers.CharField(required=True)
    new_pwd = serializers.CharField(required=True)
    model = User
