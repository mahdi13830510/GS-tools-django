import factory
from factory.django import DjangoModelFactory

from gs_tools_django.files.factories import FileFactory
from gs_tools_django.products.factories.catalog import CatalogFactory
from gs_tools_django.products.models import Image


class ImageFactory(DjangoModelFactory):
    class Meta:
        model = Image

    catalog = factory.SubFactory(CatalogFactory)
    file = factory.SubFactory(FileFactory)
    alt_text = factory.Faker("sentence", nb_words=5)
    order = factory.Sequence(lambda n: n)
