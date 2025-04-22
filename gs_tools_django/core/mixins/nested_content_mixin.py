from collections.abc import Sequence
from typing import Any

from django.contrib.contenttypes.models import ContentType
from django.db.models import Model, QuerySet
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property


class NestedContentViewMixin:
    """A mixin for DRF (or other CBVs) that restricts.

    queryset and serializer context based on one of two
    “parent” resources, selected by URL parameters.

    Attributes:
        parents_url_params: Two URL kwarg names, e.g. ["article_id", "blog_id"].
        parents_queryset: Two QuerySets to lookup those parents.
        parents_lookup_field: Field names to filter each QuerySet by.
                             Defaults to ("id", "id").
    """

    parents_url_params: Sequence[str]
    parents_queryset: Sequence[QuerySet]
    parents_lookup_field: Sequence[str] = ("id", "id")

    def _select_parent_tuple(self) -> tuple[str, str, QuerySet]:
        """Return a (parent_id, lookup_field, queryset) triple.

        Tries the second entry first; if its URL param is missing or falsy,
        falls back to the first. Raises Http404 if the first is also missing.
        """
        for idx in (1, 0):
            url_param = self.parents_url_params[idx]
            parent_id = self.kwargs.get(url_param)
            if parent_id:
                lookup_field = self.parents_lookup_field[idx]
                queryset = self.parents_queryset[idx]
                return parent_id, lookup_field, queryset

        msg = f"No parent specified. Expected one of {self.parents_url_params}"
        raise Http404(msg)

    @cached_property
    def parent(self) -> Model:
        """Fetches and caches the parent model instance based on URL kwargs."""
        parent_id, lookup_field, queryset = self._select_parent_tuple()
        return get_object_or_404(queryset, **{lookup_field: parent_id})

    @cached_property
    def parent_content_type(self) -> ContentType:
        """Caches the ContentType of the parent model for GFK lookups."""
        model_name = self.parent.__class__.__name__.lower()
        return ContentType.objects.get(model=model_name)

    def _build_parent_context(self) -> dict[str, Any]:
        """Shared data for filtering and serializer context.

        - content_type: the parent's ContentType
        - object_id:     the parent's primary key
        """
        return {
            "content_type": self.parent_content_type,
            "object_id": self.parent.pk,
        }

    def initial(self, request, *args, **kwargs) -> None:
        """Called at the start of the view; resolves the parent.

        to ensure it exists before proceeding.
        """
        super().initial(request, *args, **kwargs)
        # Access the cached_property to trigger Http404 if needed
        _ = self.parent

    def get_parent_filter_kwargs(self) -> dict[str, Any]:
        """Returns filter kwargs for `.filter(**...)` calls.

        suitable for GenericForeignKey or similar.
        """
        return self._build_parent_context()

    def get_serializer_context(self) -> dict[str, Any]:
        """Includes parent lookup data in the serializer context.

        so serializers can annotate or validate against it.
        """
        base = super().get_serializer_context()
        base.update(self._build_parent_context())
        return base

    def get_queryset(self) -> QuerySet:
        """Restricts the base queryset to objects related to the parent."""
        qs = super().get_queryset()
        return qs.filter(**self.get_parent_filter_kwargs())
