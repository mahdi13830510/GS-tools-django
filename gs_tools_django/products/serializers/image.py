from rest_framework import serializers

from gs_tools_django.products.models import Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = [
            "id",
            "file",
            "catalog",
            "order",
            "alt_text",
            "created_at",
            "modified_at",
        ]

    def create(self, validated_data):
        return Image.objects.create(catalog=self.context.get("catalog"), **validated_data)
