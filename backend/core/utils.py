from typing import TypeVar, Generic, Sequence
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
import logging
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)

T = TypeVar('T')

class PaginatedResponse(Generic[T]):
    """
    A generic pagination utility class that can be used across different endpoints.
    """
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100

    @staticmethod
    def paginate(
        request: Request,
        queryset: Sequence[T],
        serializer_class,
        search_function=None
    ) -> Response:
        """
        Paginate a queryset and return a standardized response.
        
        Args:
            request: The request object containing pagination parameters
            queryset: The queryset to paginate
            serializer_class: The serializer class to use for the queryset
            search_function: Optional function to filter queryset based on search parameter
        """
        try:
            # Get and validate pagination parameters
            page = int(request.query_params.get('page', 1))
            limit = int(request.query_params.get('limit', PaginatedResponse.DEFAULT_PAGE_SIZE))
            search = request.query_params.get('search', '').strip()

            # Validate parameters
            if page < 1:
                logger.warning("Invalid page number requested: %d", page)
                return Response(
                    {"error": "Page number must be greater than 0"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if limit < 1 or limit > PaginatedResponse.MAX_PAGE_SIZE:
                logger.warning("Invalid page size requested: %d", limit)
                return Response(
                    {"error": f"Limit must be between 1 and {PaginatedResponse.MAX_PAGE_SIZE}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Apply search if function provided
            if search and search_function:
                queryset = search_function(queryset, search)
                logger.info("Applied search filter with term: %s", search)

            # Apply pagination
            paginator = Paginator(queryset, limit)
            
            if page > paginator.num_pages and paginator.num_pages > 0:
                logger.warning("Page %d requested but only %d pages available", 
                             page, paginator.num_pages)
                return Response(
                    {"error": f"Page {page} does not exist. Total pages: {paginator.num_pages}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            page_obj = paginator.get_page(page)
            serializer = serializer_class(page_obj, many=True)

            response_data = {
                "results": serializer.data,
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total": paginator.count,
                    "total_pages": paginator.num_pages
                }
            }

            logger.info("Successfully paginated results. Page: %d, Limit: %d, Total: %d",
                       page, limit, paginator.count)

            return Response(response_data)

        except ValueError as e:
            logger.error("Invalid pagination parameters: %s", str(e))
            return Response(
                {"error": "Invalid page or limit parameter. Both must be valid numbers."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ValidationError as e:
            logger.error("Data validation error: %s", str(e))
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error("Unexpected error during pagination: %s", str(e), exc_info=True)
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )