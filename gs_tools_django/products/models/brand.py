from django.db import models
from django.utils.translation import gettext_lazy as _

from gs_tools_django.core.models import TimeStampedModel, UUIDModel
from gs_tools_django.files.models import File
from gs_tools_django.products.managers import BrandManager


class Brand(UUIDModel, TimeStampedModel):
    name = models.CharField(_("Name"), max_length=100)

    slug = models.SlugField(_("Slug"), max_length=100)

    image = models.OneToOneField(
        File,
        verbose_name=_("Image"),
        on_delete=models.CASCADE,
        related_name="brand",
    )

    objects = BrandManager()

    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")
        indexes = [
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.name
