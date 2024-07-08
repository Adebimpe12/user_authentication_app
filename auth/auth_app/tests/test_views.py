from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from user_authentication_organization_project.models import Organisation

class ViewsTestCase(TestCase):

    def setUp(self):
        # Setup a test client
        self.client = APIClient()
        
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        
        # Create a test organisation
        self.organisation = Organisation.objects.create(name='Test Organisation', owner=self.user)
    
    def test_user_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'newpassword',
            'password2': 'newpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_organisation_creation(self):
        response = self.client.post(reverse('organisation-create'), {
            'name': 'New Organisation'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_organisation_retrieval(self):
        response = self.client.get(reverse('organisation-detail', kwargs={'pk': self.organisation.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Organisation')
    
    def test_organisation_update(self):
        response = self.client.put(reverse('organisation-detail', kwargs={'pk': self.organisation.pk}), {
            'name': 'Updated Organisation'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.organisation.refresh_from_db()
        self.assertEqual(self.organisation.name, 'Updated Organisation')
    
    def test_organisation_deletion(self):
        response = self.client.delete(reverse('organisation-detail', kwargs={'pk': self.organisation.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Organisation.objects.filter(pk=self.organisation.pk).exists())
