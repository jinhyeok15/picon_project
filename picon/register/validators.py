# from django.core.exceptions import ValidationError
from .querysets import *


def validate_user(value):
    user = List.user_list()
    if value not in user:
        return False
    else:
        return True
