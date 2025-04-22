from rest_framework import serializers


class RelationshipAssignSerializer(serializers.Serializer):
    id = serializers.UUIDField()

    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop("model")
        self.field_name = kwargs.pop("field_name")
        super().__init__(*args, **kwargs)

    def validate_id(self, value):
        """Ensure the provided ID exists."""
        if not self.model.objects.filter(id=value).exists():
            msg = f"Invalid {self.model.__name__} ID: {value}"
            raise serializers.ValidationError(msg)
        return value

    def save(self, product):
        """Assign the object to the product's ManyToMany field."""
        obj = self.model.objects.get(id=self.validated_data["id"])
        getattr(product, self.field_name).add(obj)
