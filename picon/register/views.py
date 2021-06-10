from django.shortcuts import render
from django.http import Http404

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

# import re

# Create your views here.


class AccountList(generics.ListCreateAPIView):  # 계정 생성 및 조회 API
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountDetail(APIView):  # 계정 정보 조회 API
    account = AccountSerializer

    def get(self, pk):
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
        obj, created = self.queryset_object.follow_info(request, create=True)
        serializer = FollowSerializer(obj, data=request.data)

        if serializer.is_valid():
            serializer.save()
        if created:
            return Response(response_data(201, CREATED), status.HTTP_201_CREATED)
        else:
            return Response(response_data(200, UPDATED), status.HTTP_200_OK)

    def get(self, request):  # from_, to_ 필요 (쿼리 스트링)
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
