from rest_framework import viewsets, permissions
from .models import User, Group
from .serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.prefetch_related('users')
    serializer_class = GroupSerializer
    