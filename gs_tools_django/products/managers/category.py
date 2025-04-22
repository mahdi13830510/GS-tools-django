from django.db.models import Manager

from gs_tools_django.products.querysets import CategoryQuerySet


class CategoryManager(Manager):
    def get_queryset(self):
        return CategoryQuerySet(self.model, using=self._db)
