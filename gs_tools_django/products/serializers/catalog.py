from rest_framework import serializers

from gs_tools_django.products.models import Catalog
from gs_tools_django.products.serializers import ImageSerializer


class CatalogSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Catalog
        fields = [
            "id",
            "content_type",
            "object_id",
            "images",
            "created_at",
            "modified_at",
        ]
        read_only_fields = ["created_at", "modified_at", "id", "content_type", "object_id"]

    def create(self, validated_data):
        return Catalog.objects.create(
            content_type=self.context.get("content_type", None),
            object_id=self.context.get("object_id", None),
            **validated_data,
        )
