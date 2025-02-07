from django.db import models
from dongi.core.models import BaseModel
import uuid
from django.utils import timezone
from dongi.account.models import Group, User


class Expense(BaseModel):
    group = models.ForeignKey("Group", on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    bought_at = models.DateField()
    description = models.TextField(blank=True, null=True)
    
    SPLIT_TYPES = [
        ("equal", "Equal"),
        ("percentage", "Percentage"),
        ("custom", "Custom"),
    ]
    split_type = models.CharField(max_length=20, choices=SPLIT_TYPES, default="equal")
    split_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"Expense {self.id} - {self.amount}"


class ExpenseShare(BaseModel):
    expense = models.ForeignKey("Expense", on_delete=models.CASCADE, related_name="shares")
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    amount = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user} owes {self.amount} for {self.expense}"


class Payment(BaseModel):
    payer = models.ForeignKey("User", on_delete=models.CASCADE, related_name="payments_made")
    payee = models.ForeignKey("User", on_delete=models.CASCADE, related_name="payments_received")
    expense = models.ForeignKey("Expense", on_delete=models.CASCADE, null=True, blank=True)
    amount = models.FloatField(default=0)
    paid_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    receipt = models.FileField(upload_to="receipts/", blank=True, null=True)

    def __str__(self):
        return f"{self.payer} paid {self.payee} - {self.amount}"


