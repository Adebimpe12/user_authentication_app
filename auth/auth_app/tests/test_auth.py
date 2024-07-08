from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from user_authentication_organization_project.models import User
from datetime import timedelta
from django.utils import timezone

class TokenGenerationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            password='password123',
            phone='1234567890'
        )
    
    def test_token_generation(self):
        url = reverse('token_obtain_pair')
        data = {
            'email': 'john.doe@example.com',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        
        token = AccessToken(response.data['access'])
        self.assertEqual(token['user_id'], self.user.id)
        self.assertEqual(token['first_name'], self.user.first_name)
        self.assertEqual(token['last_name'], self.user.last_name)
        self.assertEqual(token['email'], self.user.email)
    
    def test_token_expiry(self):
        url = reverse('token_obtain_pair')
        data = {
            'email': 'john.doe@example.com',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        
        token = AccessToken(response.data['access'])
        expected_expiry = timezone.now() + timedelta(minutes=5)
        token_expiry = timezone.make_aware(token['exp'])
        
        self.assertAlmostEqual(expected_expiry, token_expiry, delta=timedelta(seconds=10))
