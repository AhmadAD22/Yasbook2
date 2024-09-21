import re
from rest_framework.exceptions import ValidationError

def phoneValidator(value):
    reg=r'^0\d{9}$'
    if  re.fullmatch(reg,value) is None:
        raise ValidationError("invalid phone")   

    return value