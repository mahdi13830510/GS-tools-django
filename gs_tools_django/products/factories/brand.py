import factory
from factory.django import DjangoModelFactory

from gs_tools_django.files.factories import FileFactory
from gs_tools_django.products.models import Brand


class BrandFactory(DjangoModelFactory):
    class Meta:
        model = Brand

    name = factory.Faker("company")
    slug = factory.LazyAttribute(lambda o: o.name.lower().replace(" ", "-"))
    image = factory.SubFactory(FileFactory)
