from rest_framework.viewsets import ModelViewSet

from gs_tools_django.products.models import Category
from gs_tools_django.products.serializers import CategorySerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
