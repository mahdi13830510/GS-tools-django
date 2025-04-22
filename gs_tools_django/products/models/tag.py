from django.db import models
from django.utils.translation import gettext_lazy as _

from gs_tools_django.core.models import TimeStampedModel, UUIDModel
from gs_tools_django.products.managers import TagManager


class Tag(UUIDModel, TimeStampedModel):
    name = models.CharField(_("Name"), max_length=100)

    slug = models.SlugField(_("Slug"), max_length=100)

    objects = TagManager()

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        indexes = [
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.name
