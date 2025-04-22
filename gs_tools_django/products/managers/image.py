from django.db.models import Manager

from gs_tools_django.products.querysets import ImageQuerySet


class ImageManager(Manager):
    def get_queryset(self):
        return ImageQuerySet(self.model, using=self._db)
