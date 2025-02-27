import jsonschema
from django.core.validators import BaseValidator
from django.core.exceptions import ValidationError


class JSONSchemaValidator(BaseValidator):
    def compare(self, value, schema):
        try:
            jsonschema.validate(value, schema)
        except jsonschema.ValidationError:
            raise ValidationError(f"Value {value} does not match schema")
        
