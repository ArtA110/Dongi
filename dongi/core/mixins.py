import logging
from rest_framework.pagination import PageNumberPagination

from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle


class ListCacheResponseMixin:
    """
    Mixin to cache the list response data based on query parameters.

    Attributes:
        timeout (int): Cache timeout in seconds (default: 15 minutes).

    Methods:
        get_cache_key_prefix(): Generates a unique cache key prefix based on the viewset class name.
        list(request, *args, **kwargs): Caches the serialized response data for list views.
    """
    timeout = 60 * 15  # Cache timeout in seconds

    def get_cache_key_prefix(self):
        return f"{self.__class__.__name__}_list"

    def list(self, request, *args, **kwargs):
        query_params = request.GET.urlencode()
        cache_key = f"{self.get_cache_key_prefix()}_{query_params}"
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, self.timeout)
        return response


class ThrottleMixin:
    """
    Mixin to apply scoped rate throttling to viewsets.

    Methods:
        get_throttles(): Determines the throttle scope based on the request method.
    """

    def get_throttles(self):
        if self.request.method in ["PATCH", "PUT", "POST"]:
            self.throttle_scope = "uploads"
        else:
            self.throttle_scope = "receives"
        return [ScopedRateThrottle()]


class LoggingMixin:
    """
    Mixin to log request and response details.

    Attributes:
        logger: Logger instance for logging messages.

    Methods:
        dispatch(request, *args, **kwargs): Logs request and response details.
    """
    logger = logging.getLogger(__name__)

    def dispatch(self, request, *args, **kwargs):
        user = request.user if request.user.is_authenticated else "Anonymous"
        self.logger.info(
            f"User: {user}, Request: {request.method} {request.get_full_path()}"
        )

        response = super().dispatch(request, *args, **kwargs)

        self.logger.info(
            f"User: {user}, Response: {response.status_code} {response.data}"
        )
        return response


class DefaultPaginationMixin(PageNumberPagination):
    """
    Custom pagination class with default settings.

    Attributes:
        page_size (int): Default number of items per page.
        page_size_query_param (str): Query parameter to adjust page size.
        max_page_size (int): Maximum allowed page size.
    """
    page_size = 10  # Default: 10 items per page
    page_size_query_param = 'page_size'  # e.g., ?page_size=20 to override
    max_page_size = 100  # Prevents overly large page sizes
