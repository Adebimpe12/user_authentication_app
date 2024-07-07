from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from user_authentication_organization_project.models import User, Organisation

class OrganisationAccessTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            password='password123',
            phone='1234567890'
        )
        self.user2 = User.objects.create_user(
            first_name='Jane',
            last_name='Smith',
            email='jane.smith@example.com',
            password='password123',
            phone='0987654321'
        )
        
        self.org1 = Organisation.objects.create(name="John's Org", description="")
        self.org2 = Organisation.objects.create(name="Jane's Org", description="")
        
        self.org1.users.add(self.user1)
        self.org2.users.add(self.user2)
        
        self.token_user1 = str(AccessToken.for_user(self.user1))
        self.token_user2 = str(AccessToken.for_user(self.user2))
    
    def test_user_cannot_access_other_organisation(self):
        url = reverse('organisation-detail', kwargs={'org_id': self.org2.org_id})
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user1)
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 404)  # User1 should not see User2's organisation
    
    def test_user_can_access_own_organisation(self):
        url = reverse('organisation-detail', kwargs={'org_id': self.org1.org_id})
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user1)
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)  # User1 should see their own organisation
        self.assertEqual(response.data['name'], "John's Org")
        
    def test_organisation_list_only_shows_user_organisations(self):
        url = reverse('organisation-list')
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user1)
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "John's Org")
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user2)
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Jane's Org")
