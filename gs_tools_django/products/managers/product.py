from django.db.models import Manager

from gs_tools_django.products.querysets import ProductQuerySet


class ProductManager(Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)
