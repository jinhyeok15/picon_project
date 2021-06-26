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
from picon.res import response_data, error_data
from picon.res import *
from picon.settings import AWS_STORAGE_BUCKET_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME
from picon import s3client

# import re
import uuid
from botocore.exceptions import ClientError
from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.


class AccountList(generics.ListCreateAPIView):  # 계정 생성 및 조회 API
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountDetail(APIView):  # 계정 정보 조회 API
    queryset_data = Data

    def get(self, request, pk):
        if not validate_user(pk):
            return Response(response_data(400, NOT_EXIST_USER), status.HTTP_400_BAD_REQUEST)
        data = self.queryset_data.set_profile_form(pk)
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
        data = self.queryset_data.follow_list_with_profile(pk)
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
    # file_manage_serializer = FileManageSerializer
    queryset_object = Object
    s3 = s3client.s3
    bucket_name = s3client.bucket_name

    def post(self, request, *args, **kwargs):
        user_id = request.data['user']
        if not validate_user(int(user_id)):
            return Response(response_data(400, NOT_EXIST_USER, user_id=user_id), status.HTTP_400_BAD_REQUEST)
        request_data = request.data
        try:
            file = request.FILES['file']
        except MultiValueDictKeyError as e:
            return Response(response_data(
                404, NOT_MATCH_WITH_DB,
                message="django.utils.datastructures.MultiValueDictKeyError: 'file'"),
                status.HTTP_404_NOT_FOUND
            )
        file_type = str(file).split('.')[-1]
        file_name = str(uuid.uuid1()).replace('-', '')+'.'+file_type
        if file:
            try:
                if request.data['type'] == 'image':
                    self.s3.upload_fileobj(file, self.bucket_name, file_name,
                                           ExtraArgs={'ContentType': "image/jpeg", 'ACL': "public-read"})
                elif request.data['type'] == 'video':
                    self.s3.upload_fileobj(file, self.bucket_name, file_name,
                                           ExtraArgs={'ContentType': "audio/mpeg", 'ACL': "public-read"})
                else:
                    return Response(response_data(400, NOT_VALID+"(type)"), status.HTTP_400_BAD_REQUEST)
            except ClientError as e:
                return Response(error_data(403, UPLOAD_ERROR, e.response), status.HTTP_403_FORBIDDEN)
            except S3UploadFailedError as e:
                return Response(error_data(403, UPLOAD_ERROR, e.response), status.HTTP_403_FORBIDDEN)

        data = dict()
        for key, value in request_data.items():
            if key == 'file':
                data['file_url'] = f'https://com-noc-picon.s3.ap-northeast-2.amazonaws.com/{file_name}'
            else:
                data[key] = value
        serializer = self.file_serializer(data=data)
        if serializer.is_valid():
            if int(request.data['is_profile']) == 1:  # 프로필 등록 시 기존 프로필 상태 변경
                if Data.get_profile(int(user_id), is_exist=True):
                    id_value = Data.get_profile(int(user_id))[0]['id']
                    obj = Object.get_file(id_value)
                    obj.is_profile = 0
                    obj.status = 2  # 상태 id가 2일 경우, 과거 프로필로 저장
                    obj.save()
            serializer.save()
            return Response(response_data(201, CREATED, user_id=user_id), status.HTTP_201_CREATED)
        return Response(response_data(400, NOT_VALID, data=serializer.errors), status.HTTP_400_BAD_REQUEST)

    def get(self, request):  # 삭제해야할 API
        queryset = File.objects.all()
        serializer = self.file_serializer(queryset, many=True)
        data = serializer.data
        return Response(response_data(200, OK, data=data), status.HTTP_200_OK)

    def delete(self, request):
        file_id = request.data['id']
        file_name = Data.get_file_name(file_id)
        # print(file_name)
        try:
            queryset = self.queryset_object.get_file(file_id)
        except File.DoesNotExist:
            return Response(response_data(404, DOES_NOT_EXIST), status.HTTP_404_NOT_FOUND)
        if queryset.status == 0:
            queryset.delete()
            return Response(response_data(204, DELETED), status.HTTP_204_NO_CONTENT)
        try:
            self.s3.delete_object(Bucket=self.bucket_name, Key=file_name)
            queryset.delete()
            return Response(response_data(200, DELETED), status.HTTP_200_OK)
        except ClientError as e:
            queryset.status = 0
            queryset.save()
            return Response(error_data(403, UPLOAD_ERROR, e.response, file_id=file_id, file_name=file_name),
                            status.HTTP_403_FORBIDDEN)


class UserFile(APIView):
    queryset_object = Object
    file_serializer = FileSerializer
    file_manage_serializer = FileManageSerializer

    def get(self, request, user_id):  # 유저가 가지고 있는 모든 업로드 파일 조회
        queryset = self.queryset_object.user_file(user_id)
        serializer = self.file_serializer(queryset, many=True)
        data = serializer.data
        return Response(response_data(200, OK, data=data), status.HTTP_200_OK)

    def put(self, request, user_id):  # 유저 파일 상태 변경
        file_id = request.data['id']
        if not validate_user_file(user_id, file_id):
            return Response(response_data(400, NOT_VALID), status.HTTP_400_BAD_REQUEST)
        try:
            queryset = self.queryset_object.get_file(file_id)
        except File.DoesNotExist:
            return Response(response_data(404, DOES_NOT_EXIST), status.HTTP_404_NOT_FOUND)
        serializer = self.file_manage_serializer(queryset, data=request.data)
        if serializer.is_valid():
            if request.data['is_profile'] == 1:  # 프로필 등록 시 기존 프로필 상태 변경
                if Data.get_profile(user_id, is_exist=True):
                    id_value = Data.get_profile(user_id)[0]['id']
                    print(id_value)
                    obj = Object.get_file(id_value)
                    obj.is_profile = 0
                    obj.status = 2  # 상태 id가 2일 경우, 과거 프로필로 저장
                    obj.save()
            serializer.save()
            return Response(response_data(201, UPDATED), status.HTTP_201_CREATED)
        return Response(response_data(400, NOT_VALID, data=request.data), status.HTTP_400_BAD_REQUEST)


class UserProfile(APIView):
    queryset_data = Data

    def get(self, request, user_id):
        data = self.queryset_data.get_profile(user_id, __all__=True)
        return Response(response_data(200, OK, data=data), status.HTTP_200_OK)


class UserContents(APIView):
    queryset_data = Data

    def get(self, request, user_id):
        data = self.queryset_data.user_contents(user_id)
        return Response(response_data(200, OK, data=data), status.HTTP_200_OK)
