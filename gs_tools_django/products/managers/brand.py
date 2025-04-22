from django.db.models import Manager

from gs_tools_django.products.querysets import BrandQuerySet


class BrandManager(Manager):
    def get_queryset(self):
        return BrandQuerySet(self.model, using=self._db)
