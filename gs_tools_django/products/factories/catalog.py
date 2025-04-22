import factory
from django.contrib.contenttypes.models import ContentType
from factory.django import DjangoModelFactory

from gs_tools_django.products.factories import ProductFactory
from gs_tools_django.products.models import Catalog


class CatalogFactory(DjangoModelFactory):
    class Meta:
        model = Catalog

    content_object = factory.SubFactory(ProductFactory)
    content_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.content_object)
    )
    object_id = factory.SelfAttribute("content_object.id")
