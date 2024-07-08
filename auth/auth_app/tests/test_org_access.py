from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from user_authentication_organization_project.models import Organisation  # Assuming Organisation model is in the same module

class OrganisationTests(APITestCase):

    def setUp(self):
        # Create a user and an organization
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='password123',
            first_name='John',  # Corrected from 'firstName' to 'first_name'
            last_name='Doe'     # Corrected from 'lastName' to 'last_name'
        )
        self.org = Organisation.objects.create(
            name='Test Org',
            description='Test organization'
        )
        self.user.organisations.add(self.org)

    def test_access_own_organisation(self):
        """Test access to user's own organization."""
        url = f'/api/organisations/{self.org.id}/'
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Example of a more specific assertion
        self.assertEqual(response.data['name'], 'Test Org')

    def test_access_other_organisation(self):
        """Test access to another organization (should be forbidden)."""
        other_org = Organisation.objects.create(
            name='Other Org',
            description='Another organization'
        )
        url = f'/api/organisations/{other_org.id}/'
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
