from django.shortcuts import render
from django.http import Http404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView

from .models import *
from .serializers import *


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
    def get_object(self, request, get=False, create=False):
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

    def post(self, request):
        obj, created = self.get_object(request, create=True)
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
    def follow_list(self, pk):
        serializer = FollowSerializer(Follow.objects.filter(from_follow=pk, status=1), many=True)
        l = []
        serializer_data = serializer.data
        for d in serializer_data:
            l.append(d['to_follow'])

        data = []
        for i in l:
            data.append(AccountSerializer(Account.objects.filter(id=i), many=True).data[0])
        return data

    def get(self, request, pk, format=None):
        return Response(self.follow_list(pk))

