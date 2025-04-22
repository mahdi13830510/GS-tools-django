from django.db import models
from django.utils.translation import gettext_lazy as _

from gs_tools_django.core.models import TimeStampedModel, UUIDModel
from gs_tools_django.files.models import File
from gs_tools_django.products.managers import ImageManager
from gs_tools_django.products.models import Catalog


class Image(UUIDModel, TimeStampedModel):
    catalog = models.ForeignKey(
        Catalog,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name=_("Catalog"),
    )

    file = models.OneToOneField(
        File,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name=_("File"),
    )

    alt_text = models.CharField(_("Alternative text"), max_length=255)

    order = models.PositiveIntegerField(_("Order"), default=0)

    objects = ImageManager()

    class Meta:
        ordering = ["order"]
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def __str__(self):
        return f"Image for {self.catalog} - {self.alt_text}"
