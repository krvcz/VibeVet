from django.db import models
from django.contrib.auth.models import AnonymousUser
from django.core.handlers.wsgi import WSGIRequest
import threading

_thread_local = threading.local()

def get_thread_local_request():
    """Get the current request from thread local storage."""
    return getattr(_thread_local, 'request', None)

def set_thread_local_request(request: WSGIRequest):
    """Set the current request in thread local storage."""
    _thread_local.request = request


class CustomDrugManager(models.Manager):
    """
    Custom manager for CustomDrug model to implement row-level security.
    """
    def get_queryset(self):
        user = self._get_current_user()
        if isinstance(user, AnonymousUser):
            return super().get_queryset().none()
        if user.is_superuser:
            return super().get_queryset()
        return super().get_queryset().filter(user=user)

    def _get_current_user(self):
        request = get_thread_local_request()
        if request and hasattr(request, 'user'):
            return request.user
        return AnonymousUser()


class UserSearchHistoryManager(models.Manager):
    """
    Custom manager for UserSearchHistory model to implement row-level security.
    """
    def get_queryset(self):
        user = self._get_current_user()
        if isinstance(user, AnonymousUser):
            return super().get_queryset().none()
        if user.is_superuser:
            return super().get_queryset()
        return super().get_queryset().filter(user=user)

    def _get_current_user(self):
        request = get_thread_local_request()
        if request and hasattr(request, 'user'):
            return request.user
        return AnonymousUser()