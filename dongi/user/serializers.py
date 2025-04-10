from rest_framework import serializers
from .models import User, Group
from core.serializers import PKRF


class UserSerializer(serializers.ModelSerializer):
    
    dongi_groups = serializers.StringRelatedField(many=True, read_only=True)
    
    dongi_group_ids = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        many=True,
        write_only=True,
        source='dongi_groups'
    )

    class Meta:
        model = User
        fields = "__all__"
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.context.get('limited'):
            allowed_fields = ['id', 'email', 'first_name', 'last_name']
            for field_name in list(self.fields.keys()):
                if field_name not in allowed_fields:
                    self.fields.pop(field_name)
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('password', None)
        return representation
    
    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)


class GroupSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, context={'limited': True}, read_only=True)

    class Meta:
        model = Group
        fields = "__all__"
        read_only_fields = ['id', 'deleted_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.context.get('limited'):
            allowed_fields = ['id', 'name', 'users']
            for field_name in list(self.fields.keys()):
                if field_name not in allowed_fields:
                    self.fields.pop(field_name)
    
    
        