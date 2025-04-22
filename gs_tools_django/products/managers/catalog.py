from django.db.models import Manager

from gs_tools_django.products.querysets import CatalogQuerySet


class CatalogManager(Manager):
    def get_queryset(self):
        return CatalogQuerySet(self.model, using=self._db)
