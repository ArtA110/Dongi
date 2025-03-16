from rest_framework import serializers
from .models import Notification
from user.serializers import UserSerializer
from django.core.exceptions import ValidationError


class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(context={'limited': True})

    class Meta:
        model = Notification
        fields = "__all__"
        
class SendEmailSerializer(serializers.Serializer):
    subject = serializers.CharField(required=True)
    template = serializers.FileField(required=True)
    recievers = serializers.ListField(required=True,
        child = serializers.CharField()
    )
    email_context = serializers.JSONField(required=True)
                
    def validate_template(self, value):
        if not value.name.endswith('.html'):
            raise ValidationError("Template file must be an HTML file.")
        return value
    
    def validate_email_context(self, value):
        available_values = {'first_name', 'last_name', 'role', 'dongi_groups'}
        if set(value['user']).issubset(available_values):
            return value
        raise ValidationError(f"Available Options for user are {available_values}")
