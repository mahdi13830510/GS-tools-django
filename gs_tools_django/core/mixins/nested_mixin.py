from typing import Any

from django.db.models import QuerySet
from django.http import Http404
from django.shortcuts import get_object_or_404


class NestedViewMixin:
    """A mixin for Django REST Framework viewsets to handle nested resources efficiently.

    Subclasses must define `parent_url_param` and `parent_queryset`.
    """

    parent_url_param: str  # Name of the URL parameter for the parent resource (e.g., 'category_id')
    parent_queryset: QuerySet  # Queryset for fetching the parent object
    parent_lookup_field: str = "id"  # Field used to look up the parent object (default: 'id')

    def get_parent(self) -> None:
        """Fetch the parent object based on the URL parameter and store it for reuse.

        Raises Http404 if the parent resource is not specified or not found.
        """
        parent_id = self.kwargs.get(self.parent_url_param)
        if parent_id is None:
            msg = f"Parent resource not specified for parameter: {self.parent_url_param}"
            raise Http404(msg)
        lookup_kwargs = {self.parent_lookup_field: parent_id}
        self.parent = get_object_or_404(self.parent_queryset, **lookup_kwargs)

    def get_parent_filter_kwargs(self) -> dict[str, Any]:
        """Return the filter kwargs to be used in get_queryset based on the parent object.

        By default, assumes a foreign key field named after the parent's model.
        Override this method for custom filtering, such as generic foreign keys.
        """
        parent_model_name = self.parent.__class__.__name__.lower()
        return {parent_model_name: self.parent}

    def get_serializer_context(self) -> dict[str, Any]:
        """Include the parent object in the serializer context for use in serialization."""
        context = super().get_serializer_context()
        parent_model_name = self.parent.__class__.__name__.lower()
        return {**context, parent_model_name: self.parent}

    def initial(self, request, *args, **kwargs) -> None:
        """Fetch the parent object early in the request lifecycle to validate its existence."""
        super().initial(request, *args, **kwargs)
        self.get_parent()

    def get_queryset(self) -> QuerySet:
        """Filter the queryset based on the parent object using the filter kwargs."""
        queryset = super().get_queryset()
        filter_kwargs = self.get_parent_filter_kwargs()
        return queryset.filter(**filter_kwargs)
