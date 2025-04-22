import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class UUIDModel(models.Model):
    """An abstract model that contains UUID id pk.

    This is to avoid duplicating code.
    """

    id = models.UUIDField(
        _("ID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        serialize=False,
    )

    class Meta:
        abstract = True
