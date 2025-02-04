from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from django_ulid.models import default as default_ulid
from django_ulid.models import ULIDField

def new_ulid():
    return str(default_ulid())


class User(AbstractBaseUser, PermissionsMixin):
    id = ULIDField(default=new_ulid, primary_key=True, editable=False)
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