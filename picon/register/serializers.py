from rest_framework import serializers

from .models import *

class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['id', 'nick_name', 'email', 'phone_number', 'created']

class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = ['from_follow', 'to_follow', 'status', 'modified']
