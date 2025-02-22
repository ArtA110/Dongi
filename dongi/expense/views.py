from django.shortcuts import render
from expense.models import Expense, ExpenseShare, Payment
from expense.serializers import ExpenseSerializer, ExpenseShareSerializer, PaymentSerializer
from rest_framework import viewsets

class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.select_related('group')

class ExpenseShareViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseShareSerializer
    queryset = ExpenseShare.objects.select_related('expense', 'user')

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.select_related('payer', 'payee')