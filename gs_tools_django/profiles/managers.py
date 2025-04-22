from django.db.models import Manager

from gs_tools_django.profiles.querysets import ProfileQuerySet


class ProfileManager(Manager):
    def get_queryset(self):
        return ProfileQuerySet(model=self.model, using=self._db)
