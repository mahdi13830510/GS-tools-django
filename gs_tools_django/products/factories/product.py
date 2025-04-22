import uuid

import factory
from factory.django import DjangoModelFactory

from gs_tools_django.products.factories import BrandFactory, CategoryFactory, TagFactory
from gs_tools_django.products.models import Product


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker("catch_phrase")
    category = factory.SubFactory(CategoryFactory)
    brand = factory.SubFactory(BrandFactory)
    price = factory.Faker("random_int", min=10, max=1000)
    sku = factory.LazyFunction(lambda: f"SKU-{uuid.uuid4().hex[:8]}")
    quantity_in_stock = factory.Faker("random_int", min=0, max=100)
    description = factory.Faker("paragraph")
    weight = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
    length = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
    width = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
    height = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
    meta_title = factory.Faker("sentence")
    meta_description = factory.Faker("paragraph")
    is_active = True

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.tags.add(tag)
        else:
            self.tags.add(*TagFactory.create_batch(2))
