from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from gs_tools_django.core.models import TimeStampedModel, UUIDModel
from gs_tools_django.products.managers import DiscountManager


class Discount(UUIDModel, TimeStampedModel):
    DISCOUNT_TYPE_CHOICES = [
        ("percentage", _("Percentage")),
        ("fixed", _("Fixed Amount")),
    ]

    discount_type = models.CharField(
        _("Discount Type"), max_length=10, choices=DISCOUNT_TYPE_CHOICES
    )

    value = models.DecimalField(_("Value"), max_digits=10, decimal_places=2)

    start_date = models.DateTimeField(_("Start Date"))

    end_date = models.DateTimeField(_("End Date"))

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={"app_label": "products", "model__in": ("product", "variant")},
        verbose_name=_("Content Type"),
    )

    object_id = models.UUIDField()

    content_object = GenericForeignKey("content_type", "object_id")

    objects = DiscountManager()

    class Meta:
        verbose_name = _("Discount")
        verbose_name_plural = _("Discounts")

        indexes = [
            models.Index(fields=["content_type", "object_id"]),
            models.Index(fields=["start_date", "end_date"]),
        ]

    def __str__(self):
        return f"discount for {self.content_object}"
