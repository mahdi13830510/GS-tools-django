from rest_framework.viewsets import ModelViewSet

from gs_tools_django.core.mixins import NestedViewMixin
from gs_tools_django.products.models import Catalog, Image
from gs_tools_django.products.serializers import ImageSerializer


class ImageViewSet(ModelViewSet, NestedViewMixin):
    serializer_class = ImageSerializer
    queryset = Image.objects.all().select_related("catalog", "file")
    parent_url_param = "catalog_id"
    parent_queryset = Catalog.objects.all()
    parent_lookup_field = "id"
