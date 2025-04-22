from django.db.models import Manager

from gs_tools_django.products.querysets import DiscountQuerySet


class DiscountManager(Manager):
    def get_queryset(self):
        return DiscountQuerySet(self.model, using=self._db)
