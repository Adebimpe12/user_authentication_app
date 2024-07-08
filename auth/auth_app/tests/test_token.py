from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthenticationTests(APITestCase):

    def setUp(self):
        self.user_data = {
            'email': 'testuser@example.com',
            'password': 'password123',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_token_generation_on_login(self):
        url = '/auth/login/'
        data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_token_generation_on_register(self):
        url = '/auth/register/'
        data = {
            'email': 'newuser@example.com',
            'password': 'password456',
            'first_name': 'Jane',
            'last_name': 'Smith'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
