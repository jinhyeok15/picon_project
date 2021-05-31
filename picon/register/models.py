from django.db import models

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
    from_follow = models.OneToOneField(Account, related_name='from_follow', on_delete=models.CASCADE, primary_key=True)
    to_follow = models.ManyToManyField(Account, related_name='to_follow')
    status = models.SmallIntegerField(default=1)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'follow'
