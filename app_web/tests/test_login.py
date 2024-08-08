from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse
import json 

User = get_user_model()

class LoginRequestTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.username = 'testuser'
        self.password = 'password123'
        self.email = 'testuser@example.com'
        self.user = User.objects.create_user(username=self.username, password=self.password, email=self.email)
        self.client = Client()

    def test_login_with_valid_credentials(self):
        # Simulate a POST request with valid credentials
        response = self.client.post(reverse('web:login_request'), data=json.dumps({
            'username': self.username,
            'password': self.password
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Successfully login.')

    def test_login_with_invalid_credentials(self):
        # Simulate a POST request with invalid credentials
        response = self.client.post(reverse('web:login_request'), data=json.dumps({
            'username': self.username,
            'password': 'wrongpassword'
        }), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['message'], 'Username/Email or password is incorrect.')

    def test_login_with_invalid_email(self):
        # Simulate a POST request with invalid email
        response = self.client.post(reverse('web:login_request'), data=json.dumps({
            'username': 'invalid@example.com',
            'password': self.password
        }), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['message'], 'Username/Email or password is incorrect.')

    def test_login_with_invalid_json(self):
        # Simulate a POST request with invalid JSON
        response = self.client.post(reverse('web:login_request'), data='invalidjson', content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['message'], 'Username/Email or password is incorrect.')
