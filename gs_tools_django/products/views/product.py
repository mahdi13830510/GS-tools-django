from django.db.models import Prefetch
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from gs_tools_django.products.models import Product, Tag, Variant
from gs_tools_django.products.serializers import ProductSerializer, RelationshipAssignSerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return (
            Product.objects.all()
            .with_discounted_price()
            .filter(is_active=True)
            .select_related("brand", "category")
            .prefetch_related(
                "tags",
                "related_products",
                Prefetch(
                    lookup="variants",
                    queryset=Variant.objects.all().with_discounted_price(),
                ),
            )
        )

    @action(detail=True, methods=["post"], url_path="tags")
    def assign_tag(self, request, pk=None):
        """Assign a single tag to a product."""
        serializer = RelationshipAssignSerializer(data=request.data, model=Tag, field_name="tags")
        if serializer.is_valid():
            serializer.save(self.get_object())
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors)

    @action(detail=True, methods=["post"], url_path="related-products")
    def assign_related_product(self, request, pk=None):
        """Assign a single related product to a product."""
        serializer = RelationshipAssignSerializer(
            data=request.data, model=Product, field_name="related_products"
        )
        if serializer.is_valid():
            serializer.save(self.get_object())
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=400)
