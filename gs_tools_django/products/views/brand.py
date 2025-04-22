from rest_framework.viewsets import ModelViewSet

from gs_tools_django.products.models import Brand
from gs_tools_django.products.serializers import BrandSerializer


class BrandViewSet(ModelViewSet):
    queryset = Brand.objects.all().select_related("image")
    serializer_class = BrandSerializer
