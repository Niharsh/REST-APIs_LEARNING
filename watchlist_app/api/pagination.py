from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

class WatchlistPagination(PageNumberPagination):
    page_size = 10
    # page_query_param = 'p'
    page_size_query_param = 'size'
    max_page_size = 12
    last_page_strings=['end']

class WatchlistLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 5
    max_limit = 10
    limit_query_param = 'limit'
    offset_query_param = 'start'

class WatchlistCursorPagination(CursorPagination):
    page_size = 5
    ordering = 'avg_rating'  # or '-avg_rating' for descending order
    cursor_query_param = 'cursor'