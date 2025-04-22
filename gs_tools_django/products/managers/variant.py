from django.db.models import Manager

from gs_tools_django.products.querysets import VariantQuerySet


class VariantManager(Manager):
    def get_queryset(self):
        return VariantQuerySet(self.model, using=self._db)
