import math
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response  # ✅ Add this import

class CustomPagination(PageNumberPagination):
    page_size = 2  # Default page size
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        total_items = self.page.paginator.count
        page_size = self.page.paginator.per_page
        total_pages = math.ceil(total_items / page_size) if total_items > 0 else 1

        return Response({  # ✅ Now `Response` is properly imported
            "count": total_items,
            "hasPreviousPage": self.page.has_previous(),
            "hasNextPage": self.page.has_next(),
            "pageNumber": self.page.number,
            "pageSize": page_size,
            "totalPages": total_pages,
            "results": data
        })
