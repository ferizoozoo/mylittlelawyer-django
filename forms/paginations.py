
from rest_framework.pagination import PageNumberPagination

class FormsPagination(PageNumberPagination):
    """Pagination settings for the user's forms list endpoint."""
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100
