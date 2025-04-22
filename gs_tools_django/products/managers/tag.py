from django.db.models import Manager

from gs_tools_django.products.querysets import TagQuerySet


class TagManager(Manager):
    def get_queryset(self):
        return TagQuerySet(self.model, using=self._db)
