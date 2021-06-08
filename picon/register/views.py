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

import re

# Create your views here.


class AccountList(generics.ListCreateAPIView): # 계정 생성 및 조회 API
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class AccountDetail(generics.RetrieveUpdateDestroyAPIView): # 계정 정보 조회 API
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class FollowLog(APIView):
    def get(self, request):
        queryset = Follow.objects.all()
        serializer = FollowSerializer(queryset, many=True)
        return Response(serializer.data)

class FollowInfo(APIView):
    def post(self, request):
        obj, created = Object.follow_info(request, create=True)
        serializer = FollowSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
        if created:
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status.HTTP_200_OK)

    def get(self, request):
        queryset = self.get_object(request, get=True)
        serializer = FollowSerializer(queryset)
        return Response(serializer.data)


class FollowList(APIView):
    def get(self, request, pk, format=None):
        data = Data.follow_list(pk)
        return Response(data)

class UserSearch(APIView):
    def get(self, request):
        nick_name = request.GET['nick_name']
        regex = rf'{nick_name}'
        queryset = Account.objects.filter(nick_name__iregex=regex)
        serializer = AccountSerializer(queryset, many=True)
        return Response(serializer.data)

class FollowSearch(APIView):
    def get(self, request, pk):
        nick_name = request.GET['nick_name']
        regex = rf'{nick_name}'
        search = Account.objects.filter(nick_name__iregex=regex)
        data = Data.follow_search(pk, search)
        return Response(data)
