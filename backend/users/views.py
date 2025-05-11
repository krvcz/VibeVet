import logging
from datetime import datetime
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response 
from rest_framework import status
from django.db.models import QuerySet
from django.utils.decorators import method_decorator
from common.metrics import track_metrics
from common.utils import PaginatedResponse
from users.filters import UserSearchHistoryFilter
from .models import UserSearchHistory
from .serializers import UserSearchHistorySerializer, UserSerializer
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout


logger = logging.getLogger('users')

@method_decorator(track_metrics('search_history_list'), name='list')
class SearchHistoryListView(GenericViewSet, ListModelMixin):
    """
    API endpoint for retrieving a paginated list of user's search history.
    Returns only search history for the authenticated user.
    Uses Row Level Security via UserSearchHistoryManager.
    """
    serializer_class = UserSearchHistorySerializer
    # filter_backends = [DjangoFilterBackend]
    filterset_class = UserSearchHistoryFilter

    def get_queryset(self) -> QuerySet:
        """
        Override the default queryset to filter by the authenticated user.
        This ensures that users can only see their own search history.
        """
        user = self.request.user
        if user.is_superuser:
            return UserSearchHistory.objects.order_by('-created_at')
        if user.is_authenticated:
            return UserSearchHistory.objects.filter(created_by=user).order_by('-created_at')
        return UserSearchHistory.objects.none()

class RegisterView(APIView):
    permission_classes = [] 
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        User = get_user_model()
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Create user with email as both username and email
        user = User.objects.create_user(email=email, password=password)
        login(request, user)
        return Response({'message': 'User registered and logged in successfully'}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    permission_classes = []  # Allow any user to access this view
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        User = get_user_model()
        # Try to get user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # Verify password
        user = authenticate(username=user.email, password=password)
        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        return Response({'message': 'Logged in successfully'}, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = []  # Allow any user to access this view
    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
            return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'Not logged in'}, status=status.HTTP_400_BAD_REQUEST)

class MeView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
