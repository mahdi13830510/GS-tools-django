from rest_framework import serializers

from gs_tools_django.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "phone_number", "created_at", "modified_at", "password"]
        extra_kwargs = {"password": {"write_only": True, "required": True}}
