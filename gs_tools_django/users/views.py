from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny

from gs_tools_django.users.models import User
from gs_tools_django.users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        pk = self.kwargs.get("pk")
        print(f"Attempting to retrieve object with pk: {pk}")
        try:
            obj = super().get_object()
            print(f"Object retrieved: {obj}")
            return obj
        except Exception as e:
            print(f"Lookup error: {e}")
            raise NotFound("Object not found during debugging")
