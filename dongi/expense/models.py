from django.db import models
from dongi.core.models import BaseModel
import uuid
from django.utils import timezone
from dongi.group.models import Group


class Expense(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group_id = models.ForeignKey("Group", on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    bought_at = models.DateField()
    description = models.TextField(blank=True, null=True)
    split_type = models
    split_data = models.JSONField()