from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from gs_tools_django.users.models import User
from gs_tools_django.users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
