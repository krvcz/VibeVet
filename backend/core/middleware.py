from typing import Callable
from django.http import HttpRequest, HttpResponse
from django.db import connection
from .models import set_thread_local_request

class PostgreSQLUserMiddleware:
    """
    Middleware that sets up the current user for PostgreSQL RLS policies
    and maintains thread-local request storage.
    """
    def __init__(self, get_response: Callable):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        # Store request in thread local storage for model managers
        set_thread_local_request(request)

        # Set up PostgreSQL user if authenticated
        if request.user.is_authenticated:
            with connection.cursor() as cursor:
                cursor.execute('SET LOCAL "app.current_user_id" = %s', [request.user.id])
                if request.user.is_superuser:
                    cursor.execute('SET LOCAL "app.is_admin" = true')

        response = self.get_response(request)

        return response