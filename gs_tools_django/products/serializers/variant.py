from rest_framework import serializers

from gs_tools_django.products.models import Variant


class VariantSerializer(serializers.ModelSerializer):
    discounted_price = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)

    class Meta:
        model = Variant
        fields = [
            "id",
            "product",
            "discounted_price",
            "name",
            "sku",
            "price",
            "quantity_in_stock",
        ]
        read_only_fields = ["product"]

    def create(self, validated_data):
        return Variant.objects.create(product=self.context.get("product"), **validated_data)
