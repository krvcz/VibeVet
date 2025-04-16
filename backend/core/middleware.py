from typing import Callable
from django.http import HttpRequest, HttpResponse
from django.db import connection
from django.contrib.auth.models import User
from django.contrib.auth import login
from .managers import set_thread_local_request

class MockUserMiddleware:
    """
    Development middleware that mocks a user with ID=1 for all requests.
    This is temporary and will be replaced with proper authentication.
    """
    def __init__(self, get_response: Callable):
        self.get_response = get_response
        # Cache the mock user to avoid database queries
        try:
            self.mock_user = User.objects.get(id=1)
        except User.DoesNotExist:
            # Create a mock user if it doesn't exist
            self.mock_user = User.objects.create_user(
                id=1,
                username='mockuser',
                email='mock@example.com',
                password='mockpassword123',
                is_active=True
            )

    def __call__(self, request: HttpRequest) -> HttpResponse:
        # Use Django's auth backend to properly authenticate the user
        request.user = self.mock_user
        
        # Store request in thread local storage for model managers
        set_thread_local_request(request)
        
        # Store session data
        if hasattr(request, 'session'):
            login(request, self.mock_user)
        
        response = self.get_response(request)
        return response


class PostgreSQLUserMiddleware:
    """
    Middleware that sets up the current user for PostgreSQL RLS policies.
    Must be executed AFTER MockUserMiddleware or authentication middleware.
    """
    def __init__(self, get_response: Callable):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:

         # Store request in thread local storage for model managers
        # set_thread_local_request(request)
        # Set up PostgreSQL user if authenticated
        if request.user.is_authenticated:
            with connection.cursor() as cursor:
                cursor.execute('SET LOCAL "app.current_user_id" = %s', [request.user.id])
                if request.user.is_superuser:
                    cursor.execute('SET LOCAL "app.is_admin" = true')

        response = self.get_response(request)
        return response