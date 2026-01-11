# backend/dogger/tests.py or backend/tests/test_basic.py
"""
Basic tests to verify Django setup is working
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class BasicTestCase(TestCase):
    """Basic tests to verify Django is working"""

    def test_django_is_working(self):
        """Test that Django test framework is working"""
        self.assertTrue(True)
        self.assertEqual(1 + 1, 2)

    def test_database_connection(self):
        """Test database connection by creating a user"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_basic_arithmetic(self):
        """Test basic Python functionality"""
        self.assertEqual(2 + 2, 4)
        self.assertNotEqual(2 + 2, 5)


class APITestCase(TestCase):
    """Basic API tests"""

    def setUp(self):
        """Set up test client"""
        self.client = Client()

    def test_admin_accessible(self):
        """Test that admin is accessible"""
        response = self.client.get('/admin/login/')
        # Should redirect or return 200
        self.assertIn(response.status_code, [200, 301, 302])

    # Uncomment if you have a health endpoint
    # def test_health_endpoint(self):
    #     """Test health check endpoint"""
    #     response = self.client.get('/api/health/')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json()['status'], 'healthy')


class UserModelTestCase(TestCase):
    """Tests for User model"""

    def test_create_user(self):
        """Test user creation"""
        user = User.objects.create_user(
            username='john',
            email='john@example.com',
            password='securepass123'
        )
        self.assertEqual(user.username, 'john')
        self.assertEqual(user.email, 'john@example.com')
        self.assertTrue(user.check_password('securepass123'))

    def test_user_str(self):
        """Test user string representation"""
        user = User.objects.create_user(username='jane')
        self.assertEqual(str(user), 'jane')


# For pytest
def test_basic_pytest():
    """Basic pytest test"""
    assert True
    assert 1 + 1 == 2


def test_string_operations():
    """Test string operations"""
    text = "Hello World"
    assert text.lower() == "hello world"
    assert text.upper() == "HELLO WORLD"
    assert len(text) == 11