import factory
from factory.django import DjangoModelFactory

from gs_tools_django.products.models import Category


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("word")
    slug = factory.LazyAttribute(lambda o: o.name.lower())
