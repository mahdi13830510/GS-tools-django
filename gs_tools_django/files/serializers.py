from typing import Self

from rest_framework import serializers

from gs_tools_django.files.models import File


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ["file"]

        extra_kwargs = {
            "file": {
                "required": True,
                "allow_empty_file": False,
            }
        }


class FileSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    type = serializers.CharField(source="mime_type")

    class Meta:
        model = File
        fields = ["id", "url", "type", "size", "created_by", "created_at"]
        read_only_fields = ["id", "created_at", "modified_at", "created_by", "mime_type", "url"]

    def get_url(self: Self, instance: File):
        request = self.context.get("request", None)

        if request is None:
            msg = "Request should be passed in context for this serializer"
            raise ValueError(msg)

        file_url = instance.file.url
        return request.build_absolute_uri(file_url)

    def get_size(self: Self, instance: File) -> int:
        return instance.file.size
