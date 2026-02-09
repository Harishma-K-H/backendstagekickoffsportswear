import math
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size = 20  # Default fallback
    page_number_query_param = 'pageNumber'
    page_size_query_param = 'pageSize'
    max_page_size = 200

    def get_page_number(self, request, paginator):
        try:
            return int(request.query_params.get(self.page_number_query_param, 1))
        except ValueError:
            return 1

    def get_page_size(self, request):
        # Optional override for special filters
        if request.query_params.get('branch_seaarch'):
            return 160
        try:
            page_size = int(request.query_params.get(self.page_size_query_param, self.page_size))
            return min(page_size, self.max_page_size)
        except (ValueError, TypeError):
            return self.page_size

    def paginate_queryset(self, queryset, request, view=None):
        self.request = request
        self.page_size = self.get_page_size(request)  # ✅ set it here before paginate
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        total_items = self.page.paginator.count
        total_pages = math.ceil(total_items / self.page_size) if total_items > 0 else 1

        return Response({
            "count": total_items,
            "hasPreviousPage": self.page.has_previous(),
            "hasNextPage": self.page.has_next(),
            "pageNumber": self.page.number,
            "pageSize": self.page_size,
            "totalPages": total_pages,
            "results": data
        })

