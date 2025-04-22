from django.db.models import Manager

from gs_tools_django.authentication.querysets import SMSLoginRequestQuerySet


class SMSLoginRequestManager(Manager):
    def get_queryset(self):
        return SMSLoginRequestQuerySet(self.model, using=self._db)
