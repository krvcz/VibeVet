from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserSearchHistory

# ==========================
# USER SEARCH HISTORY SERIALIZER
# ==========================

class UserSearchHistorySerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(source='created_at')

    class Meta:
        model = UserSearchHistory
        fields = [
            'id',
            'module',
            'query',
            'timestamp'
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'first_name', 'last_name')
        read_only_fields = ('id', 'email')