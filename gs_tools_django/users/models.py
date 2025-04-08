import uuid
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from gs_tools_django.users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        _("ID"),
        default=uuid.uuid4,
        primary_key=True,
        editable=False,
    )
    email = models.EmailField(
        _("Email"),
        null=True,
        blank=True,
        unique=True,
    )
    phone_number = PhoneNumberField(
        _("Phone number"),
        unique=True,
        null=False,
        blank=False,
    )
    created_at = models.DateTimeField(
        _("Created at"),
        auto_now_add=True,
        editable=False,
    )

    modified_at = models.DateTimeField(
        _("Modified at"),
        auto_now=True,
    )

    is_active = models.BooleanField(
        _("Active"),
        default=True,
    )

    password_changed_at = models.DateTimeField(_("Password changed at"), null=True)


    objects = UserManager()

    USERNAME_FIELD = "phone_number"

    def __str__(self):
        return f"{self.email} ({self.phone_number})"

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["-created_at"]

    def set_password(self, raw_password):
        super().set_password(raw_password)
        self.password_changed_at = timezone.now()