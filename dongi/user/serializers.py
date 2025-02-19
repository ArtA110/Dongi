from rest_framework import serializers
from .models import User, Group
from core.serializers import PKRF


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']


class GroupSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True)

    class Meta:
        model = Group
        fields = "__all__"
        