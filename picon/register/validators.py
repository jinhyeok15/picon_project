# from django.core.exceptions import ValidationError
from .querysets import *
from .models import *


def validate_user(value):
    user = List.user_list()
    if value not in user:
        return False
    else:
        return True


def validate_follow_relation(from_, to_):
    if from_ == to_:
        return False
    else:
        return True


def validate_user_file(user, file):
    data = Data.user_file(user)
    li = []
    for d in data:
        li.append(d['id'])
    if file in li:
        return True
    return False


def is_valid_contents(pk):
    if File.objects.filter(pk=pk, status=1, is_profile=0):
        return True
    return False

