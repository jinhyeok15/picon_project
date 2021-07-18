from django.db import models
from picon import settings
import os

# Create your models here.


class Account(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    nick_name = models.CharField(max_length=32, unique=True)
    email = models.EmailField(max_length=254, null=True, unique=True)
    phone_number = models.CharField(max_length=16, null=True, unique=True)

    class Meta:
        db_table = 'account'
        ordering = ['created']


def user_follow(pk):
    obj = Follow.objects.filter(from_follow=pk).values('to_follow')
    try:
        user_follow_list = []
        for i in obj:
            user_follow_list.append(i['to_follow'])
        return user_follow_list
    except IndexError:
        return []


def user_file(pk):
    obj = File.objects.filter(user=pk).values('id')
    try:
        user_file_list = []
        for i in obj:
            user_file_list.append(i['id'])
        return user_file_list
    except IndexError:
        return []


class Follow(models.Model):
    from_follow = models.ForeignKey('Account', related_name='user_id', on_delete=models.CASCADE)
    to_follow = models.ForeignKey('Account', related_name='follow_id', on_delete=models.CASCADE)
    status = models.SmallIntegerField(default=1)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'follow'
        constraints = [
            models.UniqueConstraint(fields=['from_follow', 'to_follow'], name='unique_relation')
        ]


class File(models.Model):
    user = models.ForeignKey('Account', related_name='user_file', on_delete=models.CASCADE)
    file_url = models.CharField(max_length=512, unique=True)
    comment = models.CharField(max_length=200, null=True)
    status = models.SmallIntegerField(default=1)  # status = 0:삭제, 1:정상, 2:과거 프로필
    created = models.DateTimeField(auto_now_add=True)
    is_profile = models.SmallIntegerField(default=0)
    type = models.CharField(max_length=10)  # 파일 업로드시 type. 'image', 'video'

    class Meta:
        db_table = 'file'


class FeedBack(models.Model):
    from_feed_back = models.ForeignKey('Account', related_name='from_feed_back', on_delete=models.CASCADE)
    to_feed_back = models.ForeignKey('File', related_name='to_feed_back', on_delete=models.CASCADE)
    # 피드백 이모티콘 종류 (heart, like, bad, sad, happy)
    type = models.CharField(max_length=10, default='heart')
    status = models.SmallIntegerField(default=1)
    modified = models.DateTimeField(auto_now=True)


class Pick(models.Model):
    from_pick = models.ForeignKey('Account', related_name='from_pick', on_delete=models.CASCADE)
    to_pick = models.ForeignKey('File', related_name='to_pick', on_delete=models.CASCADE)
    status = models.SmallIntegerField(default=1)  # 1 정상, 0 삭제
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pick'
