from rest_framework import serializers

from gs_tools_django.products.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "parent",
            "slug",
            "created_at",
            "modified_at",
        ]
