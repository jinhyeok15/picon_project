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
