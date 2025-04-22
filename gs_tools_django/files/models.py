from typing import Self

from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from gs_tools_django.core.models import TimeStampedModel, UUIDModel
from gs_tools_django.core.validators import FileSizeValidator
from gs_tools_django.users.models import User


def uploaded_file_name(instance, filename: str):
    return f"files/{instance.id}.{filename.split('.')[-1]}"


class File(UUIDModel, TimeStampedModel):
    users = models.ManyToManyField(
        User,
        related_name="files",
        verbose_name=_("Users"),
        through="UserFile",
        through_fields=("file", "user"),
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
        related_name="created_files",
        verbose_name=_("Created By"),
    )

    file = models.FileField(
        null=False,
        blank=False,
        upload_to=uploaded_file_name,
        validators=[
            FileSizeValidator(max_size=settings.ALLOWED_UPLOADED_FILE_SIZE),
            FileExtensionValidator(allowed_extensions=settings.ALLOWED_FILE_EXTENSIONS),
        ],
    )

    mime_type = models.CharField(verbose_name=_("MimeType"), blank=True, null=True)

    class Meta:
        verbose_name = _("File")
        verbose_name_plural = _("Files")
        ordering = ["-created_at"]

    def __str__(self: Self):
        return str(self.id)


class UserFile(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("User"),
    )

    file = models.ForeignKey(
        File,
        on_delete=models.CASCADE,
        verbose_name=_("File"),
    )
