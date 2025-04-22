from rest_framework import serializers

from gs_tools_django.products.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            "id",
            "name",
            "slug",
            "created_at",
            "modified_at",
        ]
