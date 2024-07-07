from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class RegisterEndpointTests(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.user_data = {
            'username': 'newuser',
            'password1': 'newpassword',
            'password2': 'newpassword',
            'first_name': 'First',
            'last_name': 'Last',
            'email': 'test@example.com'
        }

    def test_register_user(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'newuser')

    
    def test_register_user_missing_required_fields(self):
        data = {
            'first_name': '',  # Missing first_name
            'last_name': 'Test',
            'email': 'test@example.com',
            'password': 'Test1234',
            'phone': '1234567890'
        }
        response = self.client.post('/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_maximum_length_constraints(self):
        data = {
            'first_name': 'a' * 256,  # Assuming maximum length is less than 256
            'last_name': 'Test',
            'email': 'test@example.com',
            'password': 'Test1234',
            'phone': '1234567890'
        }
        response = self.client.post('/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_password_mismatch(self):
        invalid_user_data = self.user_data.copy()
        invalid_user_data['password2'] = 'differentpassword'
        
        response = self.client.post(self.register_url, invalid_user_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password2', response.data)

    def test_register_user_duplicate_username(self):
        # First registration should succeed
        self.client.post(self.register_url, self.user_data, format='json')
        # Second registration with the same username should fail
        response = self.client.post(self.register_url, self.user_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
