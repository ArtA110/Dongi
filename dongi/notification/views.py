from rest_framework import viewsets
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import SendEmailSerializer
from .utils.send_email import SendEmail
from rest_framework.permissions import AllowAny


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.select_related('user')
    serializer_class = NotificationSerializer


class SendEmailView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = SendEmailSerializer(data=request.data)

        if serializer.is_valid():
            template_file = serializer.validated_data['template']
            ulid_list = serializer.validated_data['recievers']
            subject = serializer.validated_data['subject']
            context = serializer.validated_data['email_context']
            


            se = SendEmail()
            se.send_email_with_template(subject, template_file, context, ulid_list)

            return Response({'status': 'Emails sent successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)