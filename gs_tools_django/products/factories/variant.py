import uuid

import factory
from factory.django import DjangoModelFactory

from gs_tools_django.products.factories import ProductFactory
from gs_tools_django.products.models import Variant


class VariantFactory(DjangoModelFactory):
    class Meta:
        model = Variant

    product = factory.SubFactory(ProductFactory)
    name = factory.Faker("word")
    price = factory.Faker("random_int", min=5, max=500)
    sku = factory.LazyFunction(lambda: f"VAR-{uuid.uuid4().hex[:8]}")
    quantity_in_stock = factory.Faker("random_int", min=0, max=50)
