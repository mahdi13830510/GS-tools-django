import factory
from factory.django import DjangoModelFactory

from gs_tools_django.products.models import Tag


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.Faker("word")
