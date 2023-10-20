from rest_framework import pagination
from rest_framework import status
from rest_framework.response import Response
from account.apis import messages
from .constants import (
    PAGE_SIZE,
    PAGE_SIZE_QUERY_PARAM,
    MAX_PAGE_SIZE,
    PAGE_QUERY_PARAM,
    ORDERING,
)


class CustomPagination(pagination.PageNumberPagination):
    page_size = PAGE_SIZE
    page_size_query_param = PAGE_SIZE_QUERY_PARAM
    max_page_size = MAX_PAGE_SIZE
    page_query_param = PAGE_QUERY_PARAM
    ordering = ORDERING

    def get_ordering(self, request):
        ordering = request.query_params.get("ordering", "id")

        valid_ordering_fields = [
            "project__project_name",
            "users__fullname" "status",
            "users__username",
            "id",
        ]
        if ordering.lstrip("-") not in valid_ordering_fields:
            ordering = "id"

        return ordering

    def paginate_queryset(self, queryset, request, view=None):
        offset = request.query_params.get(self.page_query_param)
        ordering = request.query_params.get("ordering", "id")

        if offset is not None:
            self.offset = offset
        if ordering is not None:
            self.ordering = ordering
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        next_url = self.get_next_link()
        prev_url = self.get_previous_link()
        ordering = self.get_ordering(self.request)

        return Response(
            {
                "count": self.page.paginator.count,
                "next": next_url,
                "previous": prev_url,
                "results": data,
                "ordering": ordering,
            }
        )


class PaginationHandlerMixin(object):
    pagination_class = CustomPagination

    @property
    def paginator(self):
        if not hasattr(self, "_paginator"):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        else:
            pass
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        page = self.paginator.page
        page_size = self.paginator.get_page_size(self.request)
        total_items = page.paginator.count
        total_pages = page.paginator.num_pages
        current_page = page.number
        previous_page = current_page - 1 if current_page > 1 else None
        next_page = current_page + 1 if current_page < total_pages else None
        return Response(
            {
                "message": messages.get_success_message(),
                "error": False,
                "code": 200,
                "results": data,
                "pagination": {
                    "total_items": total_items,
                    "total_pages": total_pages,
                    "current_page": current_page,
                    "limit": page_size,
                    "next": next_page,
                    "previous": previous_page,
                },
            },
            status=status.HTTP_200_OK,
        )
