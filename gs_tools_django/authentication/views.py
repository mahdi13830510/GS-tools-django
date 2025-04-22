from rest_framework import generics, permissions

from gs_tools_django.authentication.serializers import (
    AuthenticationSerializer,
    SMSLoginRequestSerializer,
    TokenObtainPairSerializer,
)


class SMSLoginRequestView(generics.CreateAPIView):
    serializer_class = SMSLoginRequestSerializer


class TokenObtainPairView(generics.CreateAPIView):
    serializer_class = TokenObtainPairSerializer


class AuthenticationView(generics.CreateAPIView):
    serializer_class = AuthenticationSerializer
    permission_classes = (permissions.AllowAny,)
