from rest_framework import viewsets

from gs_tools_django.products.models import Tag
from gs_tools_django.products.serializers import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
