from rest_framework.pagination import PageNumberPagination

__all__ = [
    "DinamicPagination",
]


class DinamicPagination(PageNumberPagination):
    page_size_query_param = "page_size"

    def paginate_queryset(self, queryset, request, view=None):
        if request.query_params.get("paginate", "true").lower() != "true":
            return None

        return super().paginate_queryset(queryset, request, view)
