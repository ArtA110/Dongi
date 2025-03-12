from django_ulid.models import ULIDField
from django_ulid.models import default as default_ulid
from django.db import models
from django.utils import timezone


def new_ulid():
    return str(default_ulid()) # Keeping this for migration consistency

class BaseModel(models.Model):
    id = ULIDField(default=new_ulid ,primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def soft_delete(self):
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save()

    def restore_delete(self):
        self.is_active = True
        self.deleted_at = None
        self.save()
