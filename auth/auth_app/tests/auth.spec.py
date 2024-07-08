from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from user_authentication_organization_project.models import Organisation  # Ensure your Organisation model is correctly imported

class AuthTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('token_obtain_pair')
        self.user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'password123',
            'phone': '1234567890'
        }
    def test_register_user_successfully(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
        # Check user data
        user_data = response.data['data']['user']
        self.assertEqual(user_data['first_name'], self.user_data['first_name'])
        self.assertEqual(user_data['last_name'], self.user_data['last_name'])
        self.assertEqual(user_data['email'], self.user_data['email'])

        # Check if user object exists and password is correctly set
        user = User.objects.get(email=self.user_data['email'])
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password(self.user_data['password']))

        # Check if organisation is created and user is associated
        org_name = f"{user.first_name}'s Organisation"
        organisation = Organisation.objects.filter(name=org_name).first()
        self.assertIsNotNone(organisation)
        self.assertIn(user, organisation.users.all())
    
        # Check if tokens are returned
        self.assertIn('accessToken', response.data['data'])
        self.assertIn('refreshToken', response.data['data'])

    def test_login_user_successfully(self):
        self.client.post(self.register_url, self.user_data, format='json')
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check user data
        user_data = response.data['data']['user']
        self.assertEqual(user_data['first_name'], self.user_data['first_name'])
        self.assertEqual(user_data['last_name'], self.user_data['last_name'])
        self.assertEqual(user_data['email'], self.user_data['email'])

        # Check if tokens are returned
        self.assertIn('accessToken', response.data['data'])
        self.assertIn('refreshToken', response.data['data'])

    def test_fail_if_required_fields_missing(self):
        required_fields = ['first_name', 'last_name', 'email', 'password']
        for field in required_fields:
            invalid_data = self.user_data.copy()
            del invalid_data[field]
            response = self.client.post(self.register_url, invalid_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)  # Ensure error message includes the missing field

    def test_fail_if_duplicate_email(self):
        self.client.post(self.register_url, self.user_data, format='json')
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)  # Ensure error message indicates duplicate email
