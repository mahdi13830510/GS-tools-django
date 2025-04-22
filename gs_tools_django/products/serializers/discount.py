from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from gs_tools_django.products.models import Discount


class DiscountSerializer(serializers.ModelSerializer):
    content_type = serializers.SlugRelatedField(
        queryset=ContentType.objects.filter(app_label="products", model__in=["product", "variant"]),
        slug_field="model",
    )
    object_id = serializers.UUIDField()

    class Meta:
        model = Discount
        fields = [
            "id",
            "discount_type",
            "content_type",
            "object_id",
            "value",
            "start_date",
            "end_date",
            "created_at",
            "modified_at",
        ]

    def create(self, validated_data):
        return Discount.objects.create(
            content_type=self.context.get("content_type", None),
            object_id=self.context.get("object_id", None),
            **validated_data,
        )
