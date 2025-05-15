import pytest
from django.test import TestCase
from users.tests.factories import UserFactory

pytestmark = pytest.mark.unit


class TestUserModel(TestCase):
    def test_create_user(self):
        """Test creating a regular user."""
        user = UserFactory(
            email="user@example.com",
            first_name="Test",
            last_name="User"
        )
        
        self.assertEqual(user.email, "user@example.com")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)
        
    def test_create_superuser(self):
        """Test creating a superuser."""
        admin = UserFactory(
            email="admin@example.com",
            is_staff=True,
            is_superuser=True
        )
        
        self.assertEqual(admin.email, "admin@example.com")
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_active) 