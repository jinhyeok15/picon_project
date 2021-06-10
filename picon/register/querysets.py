from .models import *
from . import serializers

# from django.shortcuts import render
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response


class List:

    @classmethod
    def follow_list(cls, pk):
        instance = Follow.objects.filter(from_follow=pk, status=1)
        serializer = serializers.FollowSerializer(instance, many=True)
        li = []
        serializer_data = serializer.data
        for d in serializer_data:
            li.append(d['to_follow'])
        return li

    @classmethod
    def user_list(cls):
        instance = Account.objects.all()
        serializer = serializers.UserSerializer(instance, many=True)
        serializer_data = serializer.data
        li = []
        for d in serializer_data:
            li.append(d['id'])
        return li


class Object:

    @classmethod
    def follow_info(cls, request, get=False, create=False):
        if get is False:
            from_ = request.data['from_follow']
            to_ = request.data['to_follow']
        else:
            from_ = request.GET['from_follow']
            to_ = request.GET['to_follow']

        try:
            if create is False:
                return Follow.objects.get(from_follow=from_, to_follow=to_)
            else:
                from_account = Account.objects.get(id=from_)
                to_account = Account.objects.get(id=to_)
                return Follow.objects.update_or_create(from_follow=from_account, to_follow=to_account)
        except Follow.DoesNotExist:
            raise Http404


class Data:

    @classmethod
    def follow_list(cls, pk):
        li = List.follow_list(pk)
        data = []
        for i in li:
            serializer = serializers.AccountSerializer(Account.objects.filter(id=i), many=True)
            data.append(serializer.data[0])
        return data

    @classmethod
    def follow_search(cls, pk, obj):
        li = List.follow_list(pk)
        data = []
        for i in li:
            serializer_data = serializers.AccountSerializer(obj.filter(id=i), many=True).data
            if not serializer_data:
                continue
            data.append(serializer_data[0])
        return data