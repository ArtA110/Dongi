from django.urls import path, include
from rest_framework.routers import DefaultRouter
from expense.views import (ExpenseViewSet, ExpenseShareViewSet, 
                           PaymentViewSet, ExpenseSplitView, ExpenseShareView)

router = DefaultRouter()
router.register(r"expenses", ExpenseViewSet)
router.register(r"expense-shares", ExpenseShareViewSet)
router.register(r"payments", PaymentViewSet)

urlpatterns = [
    path("expenses/<str:expense_id>/split/", ExpenseSplitView.as_view(), name="expense-split"),
    path("expenses/<str:expense_id>/share/", ExpenseShareView.as_view(), name="expense-share"),
    path("", include(router.urls)),
]
