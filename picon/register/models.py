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
    from_follow = models.ForeignKey('Account', related_name='user_id', on_delete=models.CASCADE)
    to_follow = models.ForeignKey('Account', related_name='follow_id', on_delete=models.CASCADE)
    status = models.SmallIntegerField(default=1)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'follow'
        constraints = [
            models.UniqueConstraint(fields=['from_follow', 'to_follow'], name='unique_relation')
        ]
