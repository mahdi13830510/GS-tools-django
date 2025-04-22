from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from gs_tools_django.core.models import TimeStampedModel, UUIDModel
from gs_tools_django.products.managers import CatalogManager


class Catalog(UUIDModel, TimeStampedModel):
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={"app_label": "products", "model__in": ("product", "variant")},
    )

    object_id = models.UUIDField()

    content_object = GenericForeignKey("content_type", "object_id")

    objects = CatalogManager()

    class Meta:
        verbose_name = _("Catalog")
        verbose_name_plural = _("Catalogs")

        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def __str__(self):
        return f"Catalog for {self.content_object}"
