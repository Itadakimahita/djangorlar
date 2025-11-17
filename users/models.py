# Python modules
from typing import Any

# Django modules
from django.db.models import (
    EmailField,
    CharField,
    BooleanField,
    DateField,
    IntegerField
)
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """
    Custom User model that extending from AbstractBaseUser
    """
    MAX_LENGTH=254
    PHONE_MAX_LENGTH=24

    email = EmailField(
        verbose_name="email address",
        max_length=MAX_LENGTH,
        unique=True,
    )
    username = CharField(
        max_length=MAX_LENGTH,
        unique=True
    )
    first_name = CharField(
        max_length=MAX_LENGTH,
    )
    last_name = CharField(
        max_length=MAX_LENGTH
    )
    phone = CharField(
        max_length=PHONE_MAX_LENGTH
    )
    city = CharField(
        max_length=MAX_LENGTH
    )
    country = CharField(
        max_length=MAX_LENGTH
    )
    department = CharField(
        max_length=MAX_LENGTH
    )
    role = CharField(
        max_length=MAX_LENGTH
    )
    birth_date = DateField(null=True)
    salary = IntegerField()
    date_joined = DateField(auto_now=True)
