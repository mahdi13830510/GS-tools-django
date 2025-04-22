from rest_framework.viewsets import ModelViewSet

from gs_tools_django.core.mixins import NestedContentViewMixin
from gs_tools_django.products.models import Catalog, Product, Variant
from gs_tools_django.products.serializers.catalog import CatalogSerializer


class CatalogViewSet(ModelViewSet, NestedContentViewMixin):
    queryset = Catalog.objects.prefetch_related("images").select_related("content_type").all()
    serializer_class = CatalogSerializer
    parents_queryset = [Product.objects.all(), Variant.objects.all()]
    parents_url_params = ["product_id", "variant_id"]
