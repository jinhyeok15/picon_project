from rest_framework.serializers import ModelSerializer
# from rest_framework.serializers import FileField

from .models import *
from .validators import *


class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'nick_name', 'email', 'phone_number', 'created']


class FollowSerializer(ModelSerializer):
    class Meta:
        model = Follow
        fields = ['from_follow', 'to_follow', 'status', 'modified']


class UserSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = ['id']


class FileSerializer(ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'


class FileManageSerializer(ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'status', 'is_profile', 'comment']
