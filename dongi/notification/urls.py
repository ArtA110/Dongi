from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet, SendEmailView

router = DefaultRouter()
router.register(r"notifications", NotificationViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("email/send/withtemplate/", SendEmailView.as_view(), name="send-email"),
]
