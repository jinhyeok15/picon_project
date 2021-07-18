from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from . import models
from .models import (
    Account, Follow, File, FeedBack, Pick
)
from . import serializers
from . import validators
from picon.res import DOES_NOT_EXIST
from rest_framework import status
from rest_framework.response import Response

from datetime import datetime, timedelta
import pytz
import re


class Element:

    @staticmethod
    def _get_obj(obj, pk, key):
        try:
            if type(pk) == list:
                element = list(map(lambda x: obj.objects.filter(pk=x).values(key), pk))
            else:
                element = obj.objects.filter(pk=pk).values(key)
            return element
        except ObjectDoesNotExist:
            raise Response(response_data(404, DOES_NOT_EXIST), status.HTTP_404_NOT_FOUND)

    @staticmethod
    def _get_element_from_obj(obj, key):
        if type(obj) == list:
            field = []
            for i in obj:
                try:
                    element = i[0][key]
                except IndexError:
                    element = None
                field.append(element)
            return field
        return obj[0][key]

    @staticmethod
    def _time_concat(time):
        now = datetime.now().replace(tzinfo=pytz.UTC)
        if not time:
            return None
        time_delta = str(now-time).replace(" ", "")
        if 'days' in time_delta:
            days = time_delta.split('days')[0]
            if 365 <= int(days):
                years = int(days)//365
                return f'{years}년 전'
            if 31 <= int(days):
                months = int(days)//30
                return f'{months}달 전'
            else:
                return f'{days}일 전'
        else:
            time_ = re.split(r'[:.]', time_delta)
            if time_[0] != '0':
                return f'{time_[0]}시간 전'
            if time_[1] != '0':
                return f'{time_[1]}분 전'
            if time_[2] != '0':
                return f'{time_[2]}초 전'
            else:
                return '지금'

    def home_contents(self, pk):  # 여러 데이터를 조회해야 하기 때문에 obj_list 요소를 가져와야 함
        user_follow_list = models.user_follow(pk)
        file_by_user_list = list(map(lambda x: models.user_file(x), user_follow_list))  # [[],[],[]]
        file_id_list = []
        try:
            for file_list in file_by_user_list:
                for i in file_list:
                    if validators.is_valid_contents(i):
                        file_id_list.append(i)
                    pass
        except IndexError:
            pass
        user_from_file_list = self._get_element_from_obj(
            list(map(lambda x: self._get_obj(File, x, 'user'), file_id_list)), 'user'
        )

        profile_url_obj = list(map(lambda x: File.objects.filter(user=x, status=1, is_profile=1).values('file_url'),
                                   user_from_file_list))
        profile_url = self._get_element_from_obj(profile_url_obj, 'file_url')
        nick_name = self._get_element_from_obj(
            self._get_obj(File, file_id_list, 'user__nick_name'), 'user__nick_name'
        )
        created = self._get_element_from_obj(
            list(map(lambda x:
                     x.filter(status=1), self._get_obj(File, file_id_list, 'created'))), 'created'
        )
        created = list(map(lambda x: self._time_concat(x), created))  # created 가공 후 재정의
        contents = self._get_element_from_obj(
            self._get_obj(File, file_id_list, 'file_url'), 'file_url'
        )
        feed_back_cnt = [len(FeedBack.objects.filter(to_feed_back=i)) for i in file_id_list]
        pick_cnt = [len(Pick.objects.filter(to_pick=i)) for i in file_id_list]
        return [profile_url, nick_name, created, contents, feed_back_cnt, pick_cnt]


class Data(Element):
    @staticmethod
    def _set_data(fields, elements):
        cnt = 0
        try:
            data_list = []
            while cnt < len(elements[0]):
                record = [i[cnt] for i in elements]
                data = dict(zip(fields, record))
                data_list.append(data)
                cnt += 1
            return data_list
        except IndexError:
            data = dict(zip(fields, elements))
            return data

    def home_contents(self, pk):
        fields = [
            'profile', 'nick_name', 'created', 'contents', 'feed_back_cnt', 'pick_cnt',
        ]
        elements = super().home_contents(pk)
        return self._set_data(fields, elements)


class Queryset(Data):
    info = '''
    Element 클래스에서 내가 원하는 요소 추출하기:
        1. queryset Obj에서 가져오기 _get_an_obj(private) (get_obj_or_404)
        만일 인자가 list라면 해당하는 리스트 목록을 조회하면서 get해서 list목록으로 return
        2. 원하는 값 받아와서 가공하기:
            만일 외래키를 참조해서 해당 obj의 pk목록을 받아오고 싶다면,
            pk = list(obj.objects.filter(fk=value).values(pk_name)) 사용
        /
    /
    Data 클래스(extends Element):
        _set_data:
            각각의 요소들을 연결해서 데이터로 바꿔 줌. (단일 요소, 리스트 요소)
        /
    /
    Queryset 클래스(extends Data):
        Data클래스로부터 data값을 전달받아 리턴하는 메소드
        or, serializers 규격에 맞춘 data리턴하는 메소드
    /
    '''
