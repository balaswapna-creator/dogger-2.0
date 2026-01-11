"""
Complete user journey integration tests
Tests real-world usage scenarios end-to-end
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
import json

User = get_user_model()

class UserJourneyTests(TestCase):
    """Test complete user workflows"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )
    
    def test_new_user_authentication_journey(self):
        """Test: New user registration and login flow"""
        
        # 1. User login (registration endpoint may not exist yet)
        response = self.client.post('/api/token/', {
            'username': 'testuser',
            'password': 'TestPass123!'
        })
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('access', data)
        self.assertIn('refresh', data)
        
        token = data['access']
        
        # 2. Access protected endpoint with token
        response = self.client.get(
            '/api/profile/',
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        self.assertEqual(response.status_code, 200)
        
        profile_data = response.json()
        self.assertEqual(profile_data['username'], 'testuser')
        self.assertEqual(profile_data['email'], 'test@example.com')
    
    def test_authentication_failure_journey(self):
        """Test: User encounters authentication errors and recovers"""
        
        # 1. Failed login attempt (wrong password)
        response = self.client.post('/api/token/', {
            'username': 'testuser',
            'password': 'WrongPassword'
        })
        self.assertEqual(response.status_code, 401)
        
        # 2. Successful login with correct credentials
        response = self.client.post('/api/token/', {
            'username': 'testuser',
            'password': 'TestPass123!'
        })
        self.assertEqual(response.status_code, 200)
        
        # 3. Verify token works
        token = response.json()['access']
        response = self.client.get(
            '/api/profile/',
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        self.assertEqual(response.status_code, 200)
    
    def test_unauthorized_access_journey(self):
        """Test: Accessing protected endpoints without authentication"""
        
        # 1. Try to access profile without token
        response = self.client.get('/api/profile/')
        self.assertEqual(response.status_code, 401)
        
        # 2. Try with invalid token
        response = self.client.get(
            '/api/profile/',
            HTTP_AUTHORIZATION='Bearer invalid_token_here'
        )
        self.assertEqual(response.status_code, 401)
        
        # 3. Get valid token and access successfully
        response = self.client.post('/api/token/', {
            'username': 'testuser',
            'password': 'TestPass123!'
        })
        token = response.json()['access']
        
        response = self.client.get(
            '/api/profile/',
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        self.assertEqual(response.status_code, 200)
    
    def test_token_refresh_journey(self):
        """Test: Token refresh workflow"""
        
        # 1. Get initial tokens
        response = self.client.post('/api/token/', {
            'username': 'testuser',
            'password': 'TestPass123!'
        })
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        refresh_token = data['refresh']
        
        # 2. Use refresh token to get new access token
        response = self.client.post('/api/token/refresh/', {
            'refresh': refresh_token
        })
        self.assertEqual(response.status_code, 200)
        
        new_data = response.json()
        self.assertIn('access', new_data)
        
        # 3. Verify new access token works
        new_token = new_data['access']
        response = self.client.get(
            '/api/profile/',
            HTTP_AUTHORIZATION=f'Bearer {new_token}'
        )
        self.assertEqual(response.status_code, 200)