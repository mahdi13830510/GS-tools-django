from rest_framework import serializers

from gs_tools_django.products.models import ProductSpecification


class ProductSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecification
        fields = [
            "id",
            "content_type",
            "object_id",
            "key",
            "value",
            "created_at",
            "modified_at",
        ]

    def create(self, validated_data):
        return ProductSpecification.objects.create(
            content_type=self.context.get("content_type", None),
            object_id=self.context.get("object_id", None),
            **validated_data,
        )
