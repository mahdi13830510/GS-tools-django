from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

from gs_tools_django.users.querysets import UserQuerySet


class UserManager(BaseUserManager):
    def get_queryset(self) -> UserQuerySet:
        return UserQuerySet(self.model, using=self._db)

    def create_user(self, phone_number, password, email=None, **extra_fields):
        """Create and save a user with the given phone number and password."""
        if not phone_number:
            # Users must have phone numbers set
            raise ValueError(_("The Phone must be set."))

        if email is not None:
            email = self.normalize_email(email)

        user = self.model(phone_number=phone_number, email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, phone_number, password=None):
        user = self.create_user(email, phone_number, password)
        user.is_admin = True
        user.save(using=self._db)
        return user
