from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from gs_tools_django.core.models import TimeStampedModel, UUIDModel
from gs_tools_django.products.managers import ProductSpecificationManager


class ProductSpecification(UUIDModel, TimeStampedModel):
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={"app_label": "products", "model__in": ("product", "variant")},
    )

    object_id = models.UUIDField()

    content_object = GenericForeignKey("content_type", "object_id")

    key = models.CharField(_("Key"), max_length=100)

    value = models.CharField(_("Value"), max_length=255)

    objects = ProductSpecificationManager()

    class Meta:
        verbose_name = _("Product Specification")
        verbose_name_plural = _("Product Specifications")

        indexes = [
            models.Index(fields=["content_type", "object_id"]),
            models.Index(fields=["key", "value"]),
        ]

    def __str__(self):
        return f"{self.content_object} - {self.key}: {self.value}"
