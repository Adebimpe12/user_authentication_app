from rest_framework import status
from rest_framework.test import APITestCase
from user_authentication_organization_project.models import User, Organisation
from django.contrib.auth.models import User

class UserEndpointsTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser', password='password123')
        self.organisation = Organisation.objects.create(name='Test Organisation', owner=self.user)


    def test_get_user_details(self):
        url = f'/api/users/{self.user.id}/'
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'testuser@example.com')

    def test_get_own_organisations(self):
        url = '/api/organisations/'
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Assuming only one organisation is created
        self.assertEqual(response.data[0]['name'], 'Test Organisation')

    def test_create_organisation(self):
        url = '/api/organisations/'
        self.client.force_authenticate(user=self.user)
        data = {'name': 'New Organisation'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Organisation.objects.count(), 2)  # Adjust count based on actual scenario
        self.assertEqual(response.data['name'], 'New Organisation')
