from rest_framework import serializers

from gs_tools_django.products.models import Brand


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = [
            "id",
            "name",
            "image",
            "slug",
            "created_at",
            "modified_at",
        ]
