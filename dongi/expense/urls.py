from django.urls import path, include
from rest_framework.routers import DefaultRouter
from expense.views import ExpenseViewSet, ExpenseShareViewSet, PaymentViewSet

router = DefaultRouter()
router.register(r"expenses", ExpenseViewSet)
router.register(r"expense-shares", ExpenseShareViewSet)
router.register(r"payments", PaymentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
