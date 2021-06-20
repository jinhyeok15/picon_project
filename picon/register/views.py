# from django.shortcuts import render
# from django.http import Http404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView

from .models import *
from .serializers import *
from .querysets import *
from .validators import *
from picon.res import response_data
from picon.res import *
from picon.settings import AWS_STORAGE_BUCKET_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

# import re
import boto3
import uuid

# Create your views here.


class AccountList(generics.ListCreateAPIView):  # 계정 생성 및 조회 API
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountDetail(APIView):  # 계정 정보 조회 API
    account = AccountSerializer

    def get(self, pk):
        if not validate_user(pk):
            return Response(response_data(400, NOT_EXIST_USER), status.HTTP_400_BAD_REQUEST)
        queryset = Account.objects.get(pk=pk)
        serializer = self.account(queryset)
        data = serializer.data
        return Response(response_data(200, OK, data=data), status.HTTP_200_OK)


class FollowLog(APIView):
    follow = FollowSerializer

    def get(self, request):
        queryset = Follow.objects.all()
        serializer = self.follow(queryset, many=True)
        data = serializer.data
        return Response(response_data(200, OK, data=data), status.HTTP_200_OK)


class FollowInfo(APIView):
    queryset_object = Object

    def post(self, request):
        from_ = request.data['from_follow']
        to_ = request.data['to_follow']

        for i in [from_, to_]:
            if not validate_user(i):
                return Response(response_data(400, NOT_EXIST_USER), status.HTTP_400_BAD_REQUEST)
        if not validate_follow_relation(from_, to_):
            return Response(response_data(400, SAME_ID), status.HTTP_400_BAD_REQUEST)

        obj, created = self.queryset_object.follow_info(request, create=True)
        serializer = FollowSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            if created:
                return Response(response_data(201, CREATED), status.HTTP_201_CREATED)
            else:
                return Response(response_data(201, UPDATED), status.HTTP_201_CREATED)
        return Response(response_data(400, NOT_VALID, data=serializer.errors), status.HTTP_400_BAD_REQUEST)

    def get(self, request):  # from_, to_ 필요 (쿼리 스트링)
        from_ = request.GET['from_follow']
        to_ = request.GET['to_follow']

        for i in [int(from_), int(to_)]:
            if not validate_user(i):
                return Response(response_data(400, NOT_EXIST_USER), status.HTTP_400_BAD_REQUEST)

        queryset = self.queryset_object.follow_info(request, get=True)
        serializer = FollowSerializer(queryset)
        data = serializer.data
        return Response(response_data(200, OK, data=data), status.HTTP_200_OK)


class FollowList(APIView):
    queryset_data = Data

    def get(self, request, pk,):
        if not validate_user(pk):
            return Response(response_data(400, NOT_EXIST_USER), status.HTTP_400_BAD_REQUEST)
        data = self.queryset_data.follow_list(pk)
        return Response(response_data(200, OK, data=data), status.HTTP_200_OK)


class UserSearch(APIView):
    account = AccountSerializer

    def get(self, request):
        nick_name = request.GET['nick_name']
        regex = rf'{nick_name}'
        queryset = Account.objects.filter(nick_name__iregex=regex)
        serializer = self.account(queryset, many=True)
        data = serializer.data
        return Response(response_data(200, OK, data=data), status.HTTP_200_OK)


class FollowSearch(APIView):
    queryset_data = Data

    def get(self, request, pk):
        nick_name = request.GET['nick_name']
        regex = rf'{nick_name}'
        search = Account.objects.filter(nick_name__iregex=regex)
        data = self.queryset_data.follow_search(pk, search)
        return Response(response_data(200, OK, data=data), status.HTTP_200_OK)


class UploadFile(APIView):
    file_serializer = FileSerializer
    file_manage_serializer = FileManageSerializer
    queryset_object = Object
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    def post(self, request, *args, **kwargs):
        user_id = request.data['user']
        request_data = request.data
        file = request.FILES['file']
        file_name = str(uuid.uuid1()).replace('-', '')
        if file:
            self.s3.upload_fileobj(file, 'com-noc-picon', file_name)
        data = dict()
        for key, value in request_data.items():
            if key == 'file':
                data['file_url'] = f'https://com-noc-picon.s3.ap-northeast-2.amazonaws.com/{file_name}'
            else:
                data[key] = value
        print(data)
        serializer = self.file_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(response_data(201, CREATED, data=serializer.data, user_id=user_id), status.HTTP_201_CREATED)
        return Response(response_data(400, NOT_VALID, data=serializer.errors), status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        queryset = File.objects.all()
        serializer = self.file_serializer(queryset, many=True)
        data = serializer.data
        return Response(response_data(200, OK, data=data), status.HTTP_200_OK)

    def delete(self, request):
        file_id = request.data['id']
        file_name = Data.get_file_name(file_id)
        queryset = self.queryset_object.get_file(file_id)
        self.s3.delete_object(Bucket='com-noc-picon', Key=file_name)
        queryset.delete()
        return Response(response_data(204, DELETED), status.HTTP_204_NO_CONTENT)
