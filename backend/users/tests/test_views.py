import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.tests.factories import UserFactory
from django.contrib.auth import get_user_model

User = get_user_model()
pytestmark = pytest.mark.integration


class TestUserViews(APITestCase):
    def setUp(self):
        self.register_url = reverse('users:register')
        self.login_url = reverse('users:login')
        
        # Prepare test data using factory but don't create the user yet
        self.test_user = UserFactory.build(
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        
        self.user_data = {
            'email': self.test_user.email,
            'password': 'testpass123',
            'first_name': self.test_user.first_name,
            'last_name': self.test_user.last_name
        }
        
    def test_user_registration(self):
        """Test that a user can register."""
        response = self.client.post(
            self.register_url,
            self.user_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'User registered and logged in successfully')
        
        # Sprawdź czy użytkownik został utworzony
        self.assertTrue(
            User.objects.filter(email=self.user_data['email']).exists()
        )
        
        # Sprawdź czy użytkownik jest zalogowany (ma sesję)
        self.assertTrue('_auth_user_id' in self.client.session)
        
    def test_user_login(self):
        """Test that a user can login."""
        # Create a user using factory
        user = UserFactory(
            email=self.user_data['email'],
            password=self.user_data['password']
        )
        
        # Then login
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        
        response = self.client.post(
            self.login_url,
            login_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Logged in successfully')
        
        # Sprawdź czy użytkownik jest zalogowany (ma sesję)
        self.assertTrue('_auth_user_id' in self.client.session)
        self.assertEqual(
            int(self.client.session['_auth_user_id']),
            user.id
        ) 