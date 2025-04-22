from django.db.models import Manager

from gs_tools_django.products.querysets import ProductSpecificationQuerySet


class ProductSpecificationManager(Manager):
    def get_queryset(self):
        return ProductSpecificationQuerySet(self.model, using=self._db)
