from django.db import models
from django.utils.translation import gettext_lazy as _

from gs_tools_django.core.models import TimeStampedModel, UUIDModel
from gs_tools_django.products.managers import CategoryManager


class Category(UUIDModel, TimeStampedModel):
    name = models.CharField(_("Name"), max_length=100)

    slug = models.SlugField(_("Slug"), max_length=100)

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="subcategories",
        verbose_name=_("Parent category"),
    )

    objects = CategoryManager()

    class Meta:
        indexes = [
            models.Index(fields=["slug"]),
        ]
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name
