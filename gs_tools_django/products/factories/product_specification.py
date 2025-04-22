import factory
from django.contrib.contenttypes.models import ContentType
from factory.django import DjangoModelFactory

from gs_tools_django.products.factories import ProductFactory
from gs_tools_django.products.models import ProductSpecification


class ProductSpecificationFactory(DjangoModelFactory):
    class Meta:
        model = ProductSpecification

    content_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.content_object)
    )
    object_id = factory.SelfAttribute("content_object.id")
    content_object = factory.SubFactory(ProductFactory)
    key = factory.Faker("word")
    value = factory.Faker("word")
