import functools
from rest_framework import serializers
from django_ulid import serializers as ulid_serializers
from user.models import User


class PKRF:
    UserPrimaryKeyRelatedField = functools.partial(
        serializers.PrimaryKeyRelatedField,
        allow_null=True,
        allow_empty=True,
        pk_field=ulid_serializers.ULIDField(),
        queryset=User.objects.all(),
    )
