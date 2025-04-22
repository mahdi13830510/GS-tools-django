from django.db import models
from django.utils.translation import gettext_lazy as _

from gs_tools_django.core.models import TimeStampedModel, UUIDModel
from gs_tools_django.profiles.managers import ProfileManager
from gs_tools_django.users.models import User


class Profile(UUIDModel, TimeStampedModel):
    """Model representing Profile instance of a User."""

    first_name = models.CharField(
        _("First Name"),
        max_length=255,
        blank=False,
        null=False,
    )

    last_name = models.CharField(
        _("Last Name"),
        max_length=255,
        blank=False,
        null=False,
    )

    username = models.CharField(
        _("Username"),
        max_length=255,
        blank=False,
        null=False,
        unique=True,
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("User"),
        related_name="profile",
    )

    objects = ProfileManager()

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
        constraints = [
            models.UniqueConstraint(name="unique_full_name", fields=["first_name", "last_name"])
        ]

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
