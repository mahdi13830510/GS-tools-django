import factory
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.utils.timezone import timedelta
from factory.django import DjangoModelFactory

from gs_tools_django.products.factories import ProductFactory
from gs_tools_django.products.models import Discount


class DiscountFactory(DjangoModelFactory):
    class Meta:
        model = Discount

    content_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.content_object)
    )
    object_id = factory.SelfAttribute("content_object.id")
    content_object = factory.SubFactory(ProductFactory)
    discount_type = factory.Iterator(["percentage", "fixed"])
    value = factory.Faker("random_int", min=5, max=50)
    start_date = factory.LazyFunction(timezone.now)
    end_date = factory.LazyFunction(lambda: timezone.now() + timedelta(days=30))
