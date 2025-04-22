from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ModelSerializer, UniqueTogetherValidator

from gs_tools_django.profiles.models import Profile


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
            "first_name",
            "last_name",
            "user",
            "username",
            "created_at",
            "modified_at",
        ]
        validators = [
            UniqueTogetherValidator(
                queryset=Profile.objects.all(),
                fields=["first_name", "last_name"],
                message=_("Another user with this name already exists."),
            )
        ]
