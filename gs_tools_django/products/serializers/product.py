from rest_framework import serializers

from gs_tools_django.products.models import Product
from gs_tools_django.products.serializers import (
    BrandSerializer,
    CategorySerializer,
    ProductSpecificationSerializer,
    TagSerializer,
    VariantSerializer,
)


class ProductSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    brand = BrandSerializer(read_only=True)
    variants = VariantSerializer(many=True, read_only=True)
    related_products = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    product_specification = ProductSpecificationSerializer(many=True, read_only=True)
    discounted_price = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "discounted_price",
            "sku",
            "quantity_in_stock",
            "weight",
            "length",
            "width",
            "height",
            "meta_title",
            "meta_description",
            "is_active",
            "tags",
            "brand",
            "variants",
            "related_products",
            "category",
            "product_specification",
            "created_at",
            "modified_at",
        ]
