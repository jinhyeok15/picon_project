from .models import *
from . import serializers

# from django.shortcuts import render
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from picon.res import DOES_NOT_EXIST


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

    @classmethod
    def is_friend(cls, pk):
        follow_list = cls.follow_list(pk)
        li = []
        for i in follow_list:
            if pk in cls.follow_list(i):
                li.append(True)
            else:
                li.append(False)
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

    @classmethod
    def get_file(cls, file_id):
        try:
            obj = File.objects.get(pk=file_id)
            return obj
        except File.DoesNotExist:
            return Response(response_data(404, DOES_NOT_EXIST), status.HTTP_404_NOT_FOUND)

    @classmethod
    def user_file(cls, user_id):
        obj = File.objects.filter(user=user_id, status__in=[1, 2])
        return obj

    @classmethod
    def upload_list(cls, user_id):
        obj = File.objects.filter(user=user_id, status=1, is_profile=0)
        return obj

    @classmethod
    def profile_list(cls, user_id, __all__=False):
        if __all__ is True:
            obj = File.objects.filter(user=user_id, status__in=[1, 2], is_profile=1)
        else:
            obj = File.objects.filter(user=user_id, status=1, is_profile=1)
        if not obj:
            obj = dict()
            return obj
        return obj


class Data:

    @classmethod
    def follow_list(cls, pk):
        li = List.follow_list(pk)
        data = []
        for i in li:
            serializer = serializers.AccountSerializer(Account.objects.filter(id=i), many=True)
            data.append(serializer.data[0])
        l_boolean = List.is_friend(pk)
        for d, b in zip(data, l_boolean):
            d['is_friend'] = b
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

    @classmethod
    def get_file_name(cls, file_id):
        obj = Object.get_file(file_id)
        serializer = serializers.FileSerializer(obj)
        data = serializer.data
        file_name = data['file_url']
        file_name = file_name.split('/')[-1]
        return file_name

    @classmethod
    def get_file_url(cls, file_id):
        obj = Object.get_file(file_id)
        serializer = serializers.FileSerializer(obj)
        data = serializer.data
        file_url = data['file_url']
        return file_url

    @classmethod
    def get_profile(cls, user_id, is_exist=False, __all__=False):
        queryset = Object.profile_list(user_id, __all__=__all__)
        serializer = serializers.FileSerializer(queryset, many=True)
        data = serializer.data
        if is_exist is True:
            if not data:
                return False
            else:
                return True
        return data

    @classmethod
    def user_file(cls, user_id):
        queryset = Object.user_file(user_id)
        serializer = serializers.FileSerializer(queryset, many=True)
        data = serializer.data
        return data

    @classmethod
    def user_contents(cls, user_id):
        queryset = Object.upload_list(user_id)
        serializer = serializers.FileSerializer(queryset, many=True)
        data = serializer.data
        return data

    @classmethod
    def set_profile_form(cls, user_id):
        try:
            queryset = Account.objects.get(pk=user_id)
        except Account.DoesNotExist:
            return Response(response_data(404, DOES_NOT_EXIST), status.HTTP_404_NOT_FOUND)
        serializer = serializers.AccountSerializer(queryset)
        data = serializer.data
        profile_data = Data.get_profile(user_id)
        try:
            data['profile_url'] = profile_data[0]['file_url']
        except IndexError:
            data['profile_url'] = None
        return data

    @classmethod
    def follow_list_with_profile(cls, user_id):
        li_follow_id = List.follow_list(user_id)
        data = []
        for i, j in zip(li_follow_id, List.is_friend(user_id)):
            account_data = Data.set_profile_form(i)
            account_data['is_friend'] = j
            data.append(account_data)
        return data


class QuerySet(List, Object, Data):

    info = {
        "List": [
            "follow_list", "user_list", "is_friend",
        ],
        "Object": [
            "follow_info", "get_file", "user_file",
            "upload_list", "profile_list",
        ],
        "Data": [
            "follow_list", "follow_search",
            "get_file_name", "get_file_url", "get_profile", "user_file", "user_contents",
            "set_profile_form", "follow_list_with_profile",
        ]
    }
