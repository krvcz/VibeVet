from typing import TypeVar, Generic, Sequence, Dict, Any, Optional, Callable, Type, Union, List, Tuple
from functools import wraps
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
import logging
import inspect
from django.core.exceptions import ValidationError, ObjectDoesNotExist

logger = logging.getLogger(__name__)

def error_response(message: str, code: Optional[str] = None, details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Create a standardized error response format.

    Args:
        message: The error message
        code: Optional error code
        details: Optional additional error details

    Returns:
        A dictionary with the standardized error format
    """
    response = {
        "error": {
            "message": message
        }
    }

    if code:
        response["error"]["code"] = code

    if details:
        response["error"]["details"] = details

    return response

# Mapping of exception types to status codes and log levels
EXCEPTION_HANDLERS = {
    # Django and DRF exceptions
    'ValidationError': (status.HTTP_400_BAD_REQUEST, logging.WARNING),
    'ObjectDoesNotExist': (status.HTTP_404_NOT_FOUND, logging.INFO),
    'PermissionDenied': (status.HTTP_403_FORBIDDEN, logging.WARNING),
    'NotAuthenticated': (status.HTTP_401_UNAUTHORIZED, logging.INFO),
    'AuthenticationFailed': (status.HTTP_401_UNAUTHORIZED, logging.WARNING),
    'NotFound': (status.HTTP_404_NOT_FOUND, logging.INFO),
    'MethodNotAllowed': (status.HTTP_405_METHOD_NOT_ALLOWED, logging.WARNING),
    'Throttled': (status.HTTP_429_TOO_MANY_REQUESTS, logging.WARNING),
    'ParseError': (status.HTTP_400_BAD_REQUEST, logging.WARNING),

    # Custom application exceptions
    'CustomDrugValidationError': (status.HTTP_400_BAD_REQUEST, logging.WARNING),
    'DrugInteractionValidationError': (status.HTTP_400_BAD_REQUEST, logging.WARNING),
    'TreatmentGuideValidationError': (status.HTTP_400_BAD_REQUEST, logging.WARNING),
    'TreatmentGuideProcessingError': (status.HTTP_500_INTERNAL_SERVER_ERROR, logging.ERROR),
    'RatingValidationError': (status.HTTP_400_BAD_REQUEST, logging.WARNING),
    'DosageCalculationError': (status.HTTP_422_UNPROCESSABLE_ENTITY, logging.WARNING),
    'UnitConversioError': (status.HTTP_422_UNPROCESSABLE_ENTITY, logging.WARNING),

    # Default handler for unhandled exceptions
    'Exception': (status.HTTP_500_INTERNAL_SERVER_ERROR, logging.ERROR)
}

def get_exception_details(exc: Exception) -> Tuple[int, int, str, Optional[Dict[str, Any]]]:
    """
    Get the status code, log level, error message, and details for an exception.

    Args:
        exc: The exception to handle

    Returns:
        Tuple containing (status_code, log_level, error_message, details)
    """
    exc_class_name = exc.__class__.__name__

    # Get status code and log level from mapping
    status_code, log_level = EXCEPTION_HANDLERS.get(
        exc_class_name,
        EXCEPTION_HANDLERS['Exception']
    )

    # Get error message
    error_message = str(exc)

    # Get details if available
    details = getattr(exc, 'detail', None)

    return status_code, log_level, error_message, details

def handle_exception(exc: Exception, log_prefix: str = "", log_exc_info: bool = True) -> Response:
    """
    Handle an exception and return an appropriate Response.

    Args:
        exc: The exception to handle
        log_prefix: Optional prefix for log messages
        log_exc_info: Whether to include exception info in log

    Returns:
        A Response object with the standardized error format
    """
    status_code, log_level, error_message, details = get_exception_details(exc)

    # Log the exception
    log_message = f"{log_prefix}{error_message}" if log_prefix else error_message
    logger.log(log_level, log_message, exc_info=log_exc_info if log_level >= logging.ERROR else False)

    # Create response
    return Response(
        error_response(
            message=error_message,
            code=exc.__class__.__name__,
            details=details
        ),
        status=status_code
    )

def try_except_decorator(func):
    """
    A decorator that wraps a function in a try-except block and handles exceptions.
    Useful for functions that are already implemented with try-except blocks.

    Usage:
        result = try_except_decorator(some_function)(arg1, arg2, ...)
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Get function name for logging
            func_name = func.__name__
            log_prefix = f"Error in {func_name}: "

            return handle_exception(e, log_prefix=log_prefix)
    return wrapper

def with_exception_handling(view_func=None, *exception_classes):
    """
    A context manager for handling exceptions in a standardized way.

    Usage:
        with with_exception_handling() as handler:
            # Your code that might raise exceptions
            result = some_function()

        # If an exception occurred, handler.response will contain the error response
        if handler.response:
            return handler.response

        # Otherwise, continue with normal processing
        return Response(result)
    """
    class ExceptionHandler:
        def __init__(self, exceptions=None):
            self.exceptions = exceptions or [Exception]
            self.response = None
            self.exc_info = None

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type is not None:
                # Check if we should handle this exception
                if any(issubclass(exc_type, exc_class) for exc_class in self.exceptions):
                    # Get caller info for logging
                    frame = inspect.currentframe().f_back
                    caller_name = frame.f_code.co_name if frame else "Unknown"
                    log_prefix = f"Error in {caller_name}: "

                    self.response = handle_exception(exc_val, log_prefix=log_prefix)
                    self.exc_info = (exc_type, exc_val, exc_tb)
                    return True  # Exception handled
            return False  # Let the exception propagate

    if view_func is None:
        return ExceptionHandler(exception_classes)

    @wraps(view_func)
    def wrapper(*args, **kwargs):
        with ExceptionHandler(exception_classes) as handler:
            return view_func(*args, **kwargs)
        if handler.response:
            return handler.response

    return wrapper

def exception_handler_decorator(*exception_classes: Type[Exception]):
    """
    Decorator for view methods to handle exceptions in a standardized way.

    Args:
        *exception_classes: Exception classes to catch. If none provided, catches all exceptions.

    Usage:
        @exception_handler_decorator(ValidationError, ObjectDoesNotExist)
        def my_view_method(self, request, *args, **kwargs):
            # Your view logic here
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            try:
                return view_func(self, request, *args, **kwargs)
            except Exception as e:
                # If specific exception classes were provided, only handle those
                if exception_classes and not any(isinstance(e, exc_class) for exc_class in exception_classes):
                    raise

                # Get view name for logging
                view_name = f"{self.__class__.__name__}.{view_func.__name__}"
                log_prefix = f"Error in {view_name}: "

                return handle_exception(e, log_prefix=log_prefix)
        return wrapper
    return decorator

def custom_exception_handler(exc: Exception, context: Dict[str, Any]) -> Optional[Response]:
    """
    Custom exception handler for DRF.

    Args:
        exc: The exception that was raised
        context: The context of the exception

    Returns:
        A Response object with the standardized error format, or None if the exception
        cannot be handled by this handler
    """
    from rest_framework.exceptions import ValidationError
    from rest_framework.views import exception_handler

    # Call DRF's default exception handler first to get the standard error response
    # response = exception_handler(exc, context)

    # Get view name for logging if available
    view = context.get('view')
    view_name = f"{view.__class__.__name__}" if view else "Unknown view"
    log_prefix = f"Error in {view_name}: "

    # If this is a ValidationError, format it according to our standard
    # if isinstance(exc, ValidationError):
    #     status_code, log_level, error_message, details = get_exception_details(exc)
    #     logger.log(log_level, f"{log_prefix}{error_message}")
    #     return Response(
    #         error_response("Validation error", code="validation_error", details=exc.detail),
    #         status=status_code
    #     )

    # For other exceptions that DRF can handle, reformat the response
    # if response is not None:
    status_code, log_level, error_message, details = get_exception_details(exc)
    logger.log(log_level, f"{log_prefix}{error_message}", exc_info=log_level >= logging.ERROR)

    error_data = error_response(
        message=str(exc),
        code=exc.__class__.__name__,
        details=getattr(exc, 'detail', None)
    )

    return Response(
        error_data,
        status=status_code
    )
 

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