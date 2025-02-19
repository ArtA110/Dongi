from rest_framework import serializers
from .models import User, Group
from core.serializers import PKRF


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ['password']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.context.get('limited'):
            allowed_fields = ['id', 'email', 'first_name', 'last_name']
            for field_name in list(self.fields.keys()):
                if field_name not in allowed_fields:
                    self.fields.pop(field_name)


class GroupSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, context={'limited': True})

    class Meta:
        model = Group
        fields = "__all__"
    
        