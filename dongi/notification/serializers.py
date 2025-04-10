from rest_framework import serializers
from .models import Notification
from user.serializers import UserSerializer
from django.core.exceptions import ValidationError
from core.validators.field_validators import JSONSchemaValidator
from user.models import User


class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(context={'limited': True}, read_only=True)
    user_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        source='user'
    )

    class Meta:
        model = Notification
        fields = "__all__"
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at']
        
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
        JSON_SCHEMA = {
            "$schema": "https://json-schema.org/draft/2020-12/schema#",
            "type": "object",
            "properties": {
                "user": {
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": ["first_name", "last_name", "dongi_groups", "role"]
                },
                "minItems": 0,
                "uniqueItems": True
                },
                "others": {
                "type": "object",
                "properties": {
                    "key": {
                    "type": "string"
                    },
                    "key2": {
                    "type": "string"
                    }
                },
                "additionalProperties": True
                }
            },
            "required": [],
            "additionalProperties": False
            }
        validator = JSONSchemaValidator()
        validator.compare(value, schema=JSON_SCHEMA)
        return value
