from django.db import models
from expense.models import Expense, ExpenseShare, Payment
from django.contrib.auth import get_user_model
from expense.serializers import (
    ExpenseSerializer,
    ExpenseShareSerializer,
    PaymentSerializer,
    ExpenseSplitSerializer,
    ExpenseSharingSerializer,
)
from rest_framework import viewsets, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from expense.utility.algorithms import DFSExpenseShareAlgorithm

User = get_user_model()


class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.select_related("group")


class ExpenseShareViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseShareSerializer
    queryset = ExpenseShare.objects.select_related("expense", "user")


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.select_related("payer", "payee")


class ExpenseSplitView(APIView):
    permission_classes = [AllowAny]

    def patch(self, request, expense_id):
        try:
            expense = Expense.objects.get(id=expense_id)
        except Expense.DoesNotExist:
            return Response(
                {"error": "Expense not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ExpenseSplitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        split_type = serializer.validated_data["split_type"]
        data = serializer.validated_data["data"]

        if split_type == "equally":
            amount = expense.amount
            split_data = {"users": []}
            users = expense.group.users.values_list("id", flat=True)
            share = amount / len(users)
            for user in users:
                split_data["users"].append({"user_id": str(user), "amount": share})
            expense.split_data = split_data
            expense.save()
        elif self._check_user_existance(data, expense):
            if split_type == "percentage":
                self._handle_percentage_split(data, expense)
            elif split_type == "custom":
                self._handle_custom_split(data, expense)
            else:
                return Response(
                    {"error": "Invalid split type"}, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"error": "Invalid user ids"}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {"message": "Expense split updated successfully"}, status=status.HTTP_200_OK
        )

    def _handle_percentage_split(self, data, expense):
        if self._check_total_amount(data, expense):
            amount = expense.amount
            split_data = {"users": []}
            for user_id, amount_p in data.items():
                split_data["users"].append(
                    {"user_id": user_id, "amount": amount * (amount_p / 100)}
                )
            expense.split_data = split_data
            expense.save()

    def _handle_custom_split(self, data, expense):
        if self._check_total_amount(data, expense, caller="custom_split"):
            split_data = {"users": []}
            for user_id, amount in data.items():
                split_data["users"].append({"user_id": user_id, "amount": amount})
            expense.split_data = split_data
            expense.save()

    def _check_total_amount(self, data, expense, caller=None):
        total_amount = ExpenseShare.objects.filter(expense=expense).aggregate(
            total_amount=models.Sum("amount")
        )["total_amount"]
        if total_amount != expense.amount:
            raise serializers.ValidationError(
                "Total amount of expense share should match the expense amount"
            )
        if caller == "custom_split":
            sum_of_custom_amounts = sum(data.values())
            if sum_of_custom_amounts != expense.amount:
                raise serializers.ValidationError(
                    "Sum of custom amounts should match the expense amount"
                )
        return True

    def _check_user_existance(self, data, expense):
        user_ids = list(data.keys())
        expense_users = list(expense.group.users.values_list("id", flat=True))
        expense_users = [str(user_id) for user_id in expense_users]
        if set(user_ids) != set(expense_users):
            raise serializers.ValidationError("Invalid user ids")
        return True


class ExpenseShareView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, expense_id):
        expense = self._fetch_expense(expense_id)
        if not expense:
            return Response(
                {"error": "Expense not found"}, status=status.HTTP_404_NOT_FOUND
            )

        split_data = expense.split_data["users"]
        expense_shares = self._fetch_shares(expense)
        if not expense_shares:
            return Response(
                {"error": "Expense not found"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        payment_data = self._process_payments(expense)
        owes, final_payments = self._calculate_shares(
            expense_shares, split_data, payment_data
        )

        transactions = self._get_transactions(final_payments, owes)
        all_user_ids = list(set(list(owes.keys()) + list(final_payments.keys())))
        user_map = self._map_users(all_user_ids)

        response_data = [
            {
                "debtor": user_map[debtor],
                "creditor": user_map[creditor],
                "amount": amount,
            }
            for debtor, creditor, amount in transactions
        ]

        serializer = ExpenseSharingSerializer(response_data, many=True)
        return Response(serializer.data)

    def _fetch_expense(self, expense_id):
        try:
            return Expense.objects.get(id=expense_id)
        except Expense.DoesNotExist:
            return None

    def _fetch_shares(self, expense):
        return ExpenseShare.objects.filter(expense=expense)

    def _process_payments(self, expense):
        payments = Payment.objects.filter(expense=expense)
        payment_data = {}

        for payment in payments:
            payer_id = str(payment.payer.id)
            payee_id = str(payment.payee.id)
            payment_data[payer_id] = payment_data.get(payer_id, 0) + payment.amount
            payment_data[payee_id] = payment_data.get(payee_id, 0) - payment.amount

        return payment_data

    def _calculate_shares(self, expense_shares, split_data, payment_data):
        owes = {i["user_id"]: i["amount"] for i in split_data}
        final_payments = {
            i["user_id"]: expense_shares.get(user=i["user_id"]).amount
            + payment_data.get(i["user_id"], 0)
            for i in split_data
        }
        return owes, final_payments

    def _get_transactions(self, final_payments, owes):
        alg = DFSExpenseShareAlgorithm()
        return alg.optimal_transactions(final_payments, owes)

    def _map_users(self, user_ids):
        all_users = User.objects.filter(id__in=user_ids)
        return {str(user.id): user for user in all_users}
