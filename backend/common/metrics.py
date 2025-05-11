import time
import logging
from functools import wraps
from typing import Any, Callable
from django.db import connection

logger = logging.getLogger(__name__)

class MetricsCollector:
    """
    Utility class for collecting and logging API metrics.
    """
    def __init__(self):
        self.start_time = None
        self.query_count_start = None
    
    def start_tracking(self) -> None:
        """Start tracking metrics for the current request"""
        self.start_time = time.perf_counter()
        self.query_count_start = len(connection.queries)
    
    def collect_metrics(self, view_name: str, status_code: int) -> dict:
        """
        Collect metrics for the current request.
        Returns a dictionary containing various performance metrics.
        """
        if not self.start_time:
            logger.warning("Metrics tracking was not started")
            return {}

        end_time = time.perf_counter()
        response_time = end_time - self.start_time
        
        # Calculate query metrics
        queries_executed = len(connection.queries) - self.query_count_start
        query_time = sum(
            float(query.get('time', 0)) 
            for query in connection.queries[self.query_count_start:]
        )

        metrics = {
            'view_name': view_name,
            'response_time': response_time,
            'status_code': status_code,
            'queries_executed': queries_executed,
            'query_time': query_time,
        }

        # Log metrics
        logger.info(
            "API Metrics - View: %(view_name)s, Response Time: %(response_time).3fs, "
            "Status: %(status_code)d, Queries: %(queries_executed)d, "
            "Query Time: %(query_time).3fs",
            metrics
        )

        return metrics


def track_metrics(view_name: str) -> Callable:
    """
    Decorator for tracking metrics of API views.
    
    Args:
        view_name: Name of the view for identification in metrics
    
    Usage:
        @api_view(['GET'])
        @track_metrics('get_drugs_list')
        def get_drugs_list(request):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            collector = MetricsCollector()
            collector.start_tracking()
            
            response = func(*args, **kwargs)
            
            collector.collect_metrics(
                view_name=view_name,
                status_code=response.status_code
            )
            
            return response
        return wrapper
    return decorator