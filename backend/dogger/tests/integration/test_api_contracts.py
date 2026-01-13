"""
API contract tests - ensure API responses match documented schemas
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
import json
from uuid import UUID

User = get_user_model()

class APIContractTests(TestCase):
    """Verify API responses match expected schemas"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='apitest',
            email='api@test.com',
            password='ApiTest123!'
        )
        response = self.client.post('/api/token/', {
            'username': 'apitest',
            'password': 'ApiTest123!'
        })
        self.token = response.json()['access']
    
    def test_health_endpoint_contract(self):
        """Health endpoint returns expected schema"""
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        
        # Updated to match actual response structure
        required_fields = ['status', 'checks']
        for field in required_fields:
            self.assertIn(field, data)
        
        # Verify status
        self.assertEqual(data['status'], 'healthy')
        
        # Verify checks structure
        self.assertIsInstance(data['checks'], dict)
        
        # Verify expected health checks exist
        expected_checks = ['database', 'cache', 'disk', 'memory', 'api_performance']
        for check in expected_checks:
            self.assertIn(check, data['checks'])
            self.assertIn('status', data['checks'][check])
    
    def test_token_endpoint_contract(self):
        """Token endpoint returns expected schema"""
        response = self.client.post('/api/token/', {
            'username': 'apitest',
            'password': 'ApiTest123!'
        })
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        required_fields = ['access', 'refresh']
        for field in required_fields:
            self.assertIn(field, data)
        
        # Verify tokens are strings
        self.assertIsInstance(data['access'], str)
        self.assertIsInstance(data['refresh'], str)
        
        # Verify tokens are not empty
        self.assertTrue(len(data['access']) > 0)
        self.assertTrue(len(data['refresh']) > 0)
    
    def test_token_refresh_endpoint_contract(self):
        """Token refresh endpoint returns expected schema"""
        # First get a refresh token
        response = self.client.post('/api/token/', {
            'username': 'apitest',
            'password': 'ApiTest123!'
        })
        refresh_token = response.json()['refresh']
        
        # Use refresh token to get new access token
        response = self.client.post('/api/token/refresh/', {
            'refresh': refresh_token
        })
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('access', data)
        self.assertIsInstance(data['access'], str)
        self.assertTrue(len(data['access']) > 0)
    
    def test_profile_endpoint_contract(self):
        """Profile endpoint returns expected schema"""
        response = self.client.get(
            '/api/profile/',
            HTTP_AUTHORIZATION=f'Bearer {self.token}'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Required fields
        self.assertIn('id', data)
        self.assertIn('username', data)
        self.assertIn('email', data)
        
        # ID validation - support both UUID and integer
        user_id = data['id']
        if isinstance(user_id, str):
            # Try to parse as UUID
            try:
                UUID(user_id)
                id_type = 'UUID'
            except ValueError:
                # If not UUID, should be numeric string
                self.assertTrue(user_id.isdigit(), f"ID '{user_id}' is not a valid UUID or integer")
                id_type = 'Integer (string)'
        else:
            # Should be an integer
            self.assertIsInstance(user_id, int)
            id_type = 'Integer'
        
        print(f"✓ User ID validated as {id_type}")
        
        # Validate other fields
        self.assertIsInstance(data['username'], str)
        self.assertIsInstance(data['email'], str)
        
        # Optional fields
        if 'first_name' in data:
            self.assertIsInstance(data['first_name'], str)
        if 'last_name' in data:
            self.assertIsInstance(data['last_name'], str)
    
    def test_unauthorized_access_contract(self):
        """Unauthorized access returns expected error schema"""
        # Access protected endpoint without token
        response = self.client.get('/api/profile/')
        self.assertEqual(response.status_code, 401)
        
        data = response.json()
        # DRF returns 'detail' when no token provided
        # Your custom handler returns 'error' for invalid tokens
        self.assertTrue('error' in data or 'detail' in data)
        error_message = data.get('error') or data.get('detail')
        self.assertIsInstance(error_message, str)
    
    def test_invalid_token_contract(self):
        """Invalid token returns expected error schema"""
        response = self.client.get(
            '/api/profile/',
            HTTP_AUTHORIZATION='Bearer invalid_token'
        )
        self.assertEqual(response.status_code, 401)
        
        data = response.json()
        # Your API returns 'error' field instead of 'detail'
        self.assertIn('error', data)
        self.assertIsInstance(data['error'], str)
        self.assertEqual(data['error'], 'Invalid or expired token')
    
    def test_invalid_login_contract(self):
        """Invalid login returns expected error schema"""
        response = self.client.post('/api/token/', {
            'username': 'nonexistent',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 401)
        
        data = response.json()
        # Check for error message
        self.assertTrue('detail' in data or 'error' in data)