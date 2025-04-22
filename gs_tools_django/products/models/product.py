from django.db import models
from django.utils.translation import gettext_lazy as _

from gs_tools_django.core.models import TimeStampedModel, UUIDModel
from gs_tools_django.products.managers import ProductManager
from gs_tools_django.products.models import Brand, Category, Tag


class Product(UUIDModel, TimeStampedModel):
    name = models.CharField(_("Name"), max_length=255)

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name=_("Category"),
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name=_("Brand"),
    )

    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)

    sku = models.CharField(_("SKU"), max_length=50, unique=True)

    quantity_in_stock = models.PositiveIntegerField(_("Quantity in stock"))

    description = models.TextField(_("Description"), blank=True)

    weight = models.DecimalField(
        _("Weight"), max_digits=10, decimal_places=2, null=True, blank=True
    )

    length = models.DecimalField(
        _("Length"), max_digits=10, decimal_places=2, null=True, blank=True
    )

    width = models.DecimalField(_("Width"), max_digits=10, decimal_places=2, null=True, blank=True)

    height = models.DecimalField(
        _("Height"), max_digits=10, decimal_places=2, null=True, blank=True
    )

    meta_title = models.CharField(_("Meta Title"), max_length=255, blank=True)

    meta_description = models.TextField(_("Meta Description"), blank=True)

    tags = models.ManyToManyField(Tag, related_name="products", blank=True, verbose_name=_("Tags"))

    related_products = models.ManyToManyField(
        "self",
        blank=True,
        symmetrical=False,
        related_name="related_to",
        verbose_name=_("Related products"),
    )

    is_active = models.BooleanField(_("Is Active"), default=True)

    objects = ProductManager()

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["sku"]),
        ]

    def __str__(self):
        return self.name
