import factory
from factory.django import DjangoModelFactory

from gs_tools_django.files.models import File
from gs_tools_django.users.factories import UserFactory


class FileFactory(DjangoModelFactory):
    class Meta:
        model = File

    created_by = factory.SubFactory(UserFactory)
    file = factory.django.FileField(filename="test.jpg", data=b"dummy image content")
    mime_type = "image/jpeg"
