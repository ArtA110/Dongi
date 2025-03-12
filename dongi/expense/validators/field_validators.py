import jsonschema
from django.core.validators import BaseValidator
from django.core.exceptions import ValidationError


class JSONSchemaValidator(BaseValidator):
    def compare(self, value, schema):
        try:
            jsonschema.validate(value, schema)
        except jsonschema.ValidationError:
            raise ValidationError(f"Value {value} does not match schema")
        
        
def validate_split_data(split_data, amount):
   
    if split_data:
        users = split_data.get('users', [])
        total_amount = sum(user['amount'] for user in users)
        if total_amount != amount:
            raise ValidationError(
                f"The sum of amounts in split_data ({total_amount}) does not match the expense amount ({amount})."
            )
            