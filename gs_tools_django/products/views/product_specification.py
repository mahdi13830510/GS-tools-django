from rest_framework.viewsets import ModelViewSet

from gs_tools_django.core.mixins import NestedContentViewMixin
from gs_tools_django.products.models import Product, ProductSpecification, Variant
from gs_tools_django.products.serializers import ProductSpecificationSerializer


class ProductSpecificationViewSet(ModelViewSet, NestedContentViewMixin):
    queryset = ProductSpecification.objects.all()
    serializer_class = ProductSpecificationSerializer
    parents_queryset = [Product.objects.all(), Variant.objects.all()]
    parents_url_params = ["product_id", "variant_id"]
