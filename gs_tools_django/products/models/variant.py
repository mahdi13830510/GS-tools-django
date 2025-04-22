from django.db import models
from django.utils.translation import gettext_lazy as _

from gs_tools_django.core.models import TimeStampedModel, UUIDModel
from gs_tools_django.products.managers import VariantManager
from gs_tools_django.products.models import Product


class Variant(UUIDModel, TimeStampedModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants",
        verbose_name=_("Product"),
    )

    name = models.CharField(_("Name"), max_length=100)

    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)

    sku = models.CharField(_("SKU"), max_length=50, unique=True)

    quantity_in_stock = models.PositiveIntegerField(_("Quantity in stock"))

    objects = VariantManager()

    class Meta:
        verbose_name = _("Variant")
        verbose_name_plural = _("Variants")

    def __str__(self):
        return f"{self.product.name} - {self.name}"
