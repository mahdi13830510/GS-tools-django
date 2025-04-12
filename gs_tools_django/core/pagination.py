from typing import Self

from rest_framework import pagination
from rest_framework.response import Response


class PageSizePagination(pagination.PageNumberPagination):
    page_size_query_param = "page_size"
    page_query_param = "page"
    page_size = 25  # TODO: read default value from environment variables.
    max_page_size = 100

    def get_paginated_response(self: Self, data):
        return Response(
            {
                "total_items": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "current_page": self.page.number,
                "per_page": self.page.paginator.per_page,
                "items": data,
            },
        )