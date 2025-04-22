from rest_framework.viewsets import ModelViewSet

from gs_tools_django.core.mixins import NestedViewMixin
from gs_tools_django.products.models import Product, Variant
from gs_tools_django.products.serializers import VariantSerializer


class VariantViewSet(ModelViewSet, NestedViewMixin):
    serializer_class = VariantSerializer
    parent_queryset = Product.objects.all()
    parent_url_param = "product_id"

    def get_queryset(self):
        return Variant.objects.all().with_discounted_price()
