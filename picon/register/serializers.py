from rest_framework.serializers import ModelSerializer

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
        fields = ['id', 'user', 'file', 'status', 'created', 'is_profile']


class FileManageSerializer(ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'status', 'is_profile']
