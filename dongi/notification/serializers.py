from rest_framework import serializers
from .models import Notification
from user.serializers import UserSerializer


class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(context={'limited': True})

    class Meta:
        model = Notification
        fields = "__all__"
