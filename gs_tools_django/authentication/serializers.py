from django.utils.translation import gettext_lazy as _
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from gs_tools_django.authentication.models import SMSLoginRequest
from gs_tools_django.users.models import User


class SMSLoginRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSLoginRequest
        fields = ["id", "phone_number", "created_at", "expires_at"]
        extra_kwargs = {
            "id": {"read_only": True},
            "expires_at": {"read_only": True},
            "created_at": {"read_only": True},
        }

    def create(self, validated_data):
        request = SMSLoginRequest.objects.create(**validated_data)
        request.send()
        request.save()
        return request


class TokenObtainPairSerializer(serializers.Serializer):
    """Serializer to create a pair of refresh token and access token for user."""

    code = serializers.IntegerField(required=True, write_only=True)
    request_id = serializers.UUIDField(required=True, write_only=True)
    otp_type = serializers.CharField(required=True, write_only=True)

    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs: dict[str, str]) -> dict[str, str]:
        otp_type = attrs.get("otp_type")
        request_id = attrs.get("request_id")
        code = attrs.get("code")

        if otp_type == "S":
            request = SMSLoginRequest.objects.filter(id=request_id, code=code).valid()
            if not request.exists():
                msg = _("Code or request id is invalid.")
                raise serializers.ValidationError(msg)
            user = User.objects.filter(phone_number=request.phone_number).first()
            if user is None or not user.is_active:
                msg = _("No active account found with the given credentials.")
                raise serializers.ValidationError(msg)
            self.user = user
            return super().validate(attrs)

        return super().validate(attrs)

    def save(self) -> dict[str, str]:
        token = RefreshToken.for_user(self.user)

        self.instance = {"access": str(token.access_token), "refresh": str(token)}

        return self.instance


class AuthenticationSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)

    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs: dict[str, str]) -> dict[str, str]:
        phone_number = attrs.get("phone_number")
        password = attrs.get("password")
        try:
            user = User.objects.get(phone_number=phone_number, password=password)
            username = user.phone_number  # Get the username linked to this phone number
        except User.DoesNotExist:
            msg = _("No active account found with this phone number.")
            raise serializers.ValidationError(msg) from None

        self.user = user
        return super().validate(attrs)

    def save(self) -> dict[str, str]:
        token = RefreshToken.for_user(self.user)
        # Sorry for the dirty work here. SimpleJWT itself is a mess anyway. I did this to have only
        # a single serializer and use CreateView.
        self.instance = {"access": str(token.access_token), "refresh": str(token)}
        return self.instance
