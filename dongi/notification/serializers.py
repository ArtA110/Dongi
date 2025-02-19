from rest_framework import serializers
from .models import Notification
from core.serializers import PKRF


class NotificationSerializer(serializers.ModelSerializer):
    user = PKRF.UserPrimaryKeyRelatedField()

    class Meta:
        model = Notification
        fields = "__all__"
