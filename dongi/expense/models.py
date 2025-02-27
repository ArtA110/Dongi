from django.db import models
from core.models import BaseModel
from user.models import Group
from django.contrib.auth import get_user_model
from .validators.field_validators import JSONSchemaValidator, validate_split_data

User = get_user_model()


SPLIT_DATA_JSON_SCHEMA = {
  "$schema": "https://json-schema.org/draft/2020-12/schema#",
  "type": "object",
  "properties": {
    "users": {
      "type": "array",
      "description": "List of users and their respective amounts",
      "items": {
        "type": "object",
        "properties": {
          "user_id": {
            "type": "string",
            "description": "User ID of the user"
          },
          "amount": {
            "type": "number",
            "description": "Amount that should be paid by the user"
          }
        },
        "required": ["user_id", "amount"]
      }
    }
  },
  "required": ["users"]
}
class Expense(BaseModel):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    bought_at = models.DateField()
    description = models.TextField(blank=True, null=True)
    split_data = models.JSONField(validators=[JSONSchemaValidator(limit_value=SPLIT_DATA_JSON_SCHEMA)],
                                  blank=True, null=True)
    factor = models.ImageField(upload_to="factors/", blank=True, null=True)

    def __str__(self):
        return f"Expense {self.id} - {self.amount}"
    
    def clean(self):
        validate_split_data(self.split_data, self.amount)
        return super().clean()
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class ExpenseShare(BaseModel):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name="shares")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    amount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user} owes {self.amount} for {self.expense}"


class Payment(BaseModel):
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments_made")
    payee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments_received")
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    paid_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    receipt = models.ImageField(upload_to="receipts/", blank=True, null=True)

    def __str__(self):
        return f"{self.payer} paid {self.payee} - {self.amount}"
