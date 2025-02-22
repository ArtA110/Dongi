from django.contrib import admin
from expense.models import Expense, ExpenseShare, Payment

admin.site.register(Expense)
admin.site.register(ExpenseShare)
admin.site.register(Payment)
