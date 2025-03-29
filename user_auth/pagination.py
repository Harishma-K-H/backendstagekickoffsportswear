import math
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size = 20 # Default page size
    page_number_query_param = 'pageNumber'  # Use 'pageNumber' instead of 'page'
    page_size_query_param = 'pageSize'  # Allow changing page size dynamically
    max_page_size = 100

    def get_page_number(self, request, paginator):
        """
        Override to use 'pageNumber' instead of 'page'
        """
        try:
            return int(request.query_params.get(self.page_number_query_param, 1))
        except ValueError:
            return 1  # Default to page 1 if invalid pageNumber is given

    def get_page_size(self, request):
        """
        Override to fetch 'pageSize' dynamically instead of using a fixed value
        """
        try:
            return int(request.query_params.get(self.page_size_query_param, self.page_size))
        except (ValueError, TypeError):
            return self.page_size  # Fallback to default page size

    def get_paginated_response(self, data):
        total_items = self.page.paginator.count
        page_size = self.get_page_size(self.request)  # Fetch dynamic page size
        total_pages = math.ceil(total_items / page_size) if total_items > 0 else 1

        return Response({
            "count": total_items,
            "hasPreviousPage": self.page.has_previous(),
            "hasNextPage": self.page.has_next(),
            "pageNumber": self.page.number,
            "pageSize": page_size,
            "totalPages": total_pages,
            "results": data
        })
