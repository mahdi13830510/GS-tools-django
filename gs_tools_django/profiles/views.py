from rest_framework import permissions, viewsets

from gs_tools_django.profiles.models import Profile
from gs_tools_django.profiles.serializers import ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
