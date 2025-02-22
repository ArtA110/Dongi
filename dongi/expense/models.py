from django.db import models
from core.models import BaseModel
from user.models import Group
from django.contrib.auth import get_user_model

User = get_user_model()
class Expense(BaseModel):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    bought_at = models.DateField()
    description = models.TextField(blank=True, null=True)
    split_data = models.JSONField(blank=True, null=True)
    factor = models.ImageField(upload_to="factors/", blank=True, null=True)

    def __str__(self):
        return f"Expense {self.id} - {self.amount}"


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
