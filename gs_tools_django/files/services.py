import mimetypes
from typing import Self

from django.core.files.uploadhandler import InMemoryUploadedFile
from django.db import transaction

from gs_tools_django.files.models import File, UserFile
from gs_tools_django.users.models import User


def _infer_file_name_and_type(file_obj: InMemoryUploadedFile) -> tuple[str, str]:
    file_name = file_obj.name

    guessed_file_type, _ = mimetypes.guess_type(file_name)
    file_type = guessed_file_type or ""

    return file_name, file_type


class FileService:
    def __init__(self: Self, user: User):
        self.user = user

    def create_file_for_user(self: Self, file: File) -> File:
        with transaction.atomic():
            _, guessed_type = _infer_file_name_and_type(file)

            file = File.objects.create(
                created_by=self.user,
                file=file,
                mime_type=guessed_type,
            )
            UserFile.objects.create(user=self.user, file=file)
        return file
