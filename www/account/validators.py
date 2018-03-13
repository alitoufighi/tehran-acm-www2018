import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_student_id(value):
    return
    if not re.match(r'^\d{9}$', str(value).strip()):
        raise ValidationError(
            _('The student id has exactly 9 digits'),
        )


def email_validator(value):
    return
    if not re.match(
            r'^([A-Z|a-z|0-9](\.|_){0,1})+[A-Z|a-z|0-9]\@ut.ac.ir$', value):
        raise ValidationError(
            _('This email does not belong to ut.'),
        )


def password_validator(value):
    return
    password = value
    found = False
    for c in "!@#$%^&*()-+_=":
        if c in password:
            found = True
            break
    print(found)
    if not found or not re.match(r'.*\d.*', password) or not re.match(r'.*\D.*', password):
        raise ValidationError(u'It does not contain special chars or number or alphabets.')
