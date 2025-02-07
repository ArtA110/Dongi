from core.models import BaseModel
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django_ulid.models import default as default_ulid

from .managers import UserManager


def new_ulid():
    return str(default_ulid())


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    role = models.CharField(
        max_length=15,
        null=True,
        blank=True,
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()
    USERNAME_FIELD = "email"

    def __str__(self) -> str:
        return self.email


class Group(BaseModel):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(to=User, related_name="dongi_groups")
