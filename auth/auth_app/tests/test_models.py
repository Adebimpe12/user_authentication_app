from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserModelTestCase(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.assertIsNotNone(user.pk)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
