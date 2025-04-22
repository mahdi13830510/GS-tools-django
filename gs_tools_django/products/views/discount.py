from rest_framework.viewsets import ModelViewSet

from gs_tools_django.core.mixins import NestedContentViewMixin
from gs_tools_django.products.models import Discount, Product, Variant
from gs_tools_django.products.serializers import DiscountSerializer


class DiscountViewSet(ModelViewSet, NestedContentViewMixin):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    parents_queryset = [Product.objects.all(), Variant.objects.all()]
    parents_url_params = ["product_id", "variant_id"]
