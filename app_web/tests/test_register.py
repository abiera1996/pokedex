from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
import json
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class RegisterRequestTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_with_valid_data(self):
        # Simulate a POST request with valid data
        response = self.client.post(reverse('web:register_request'), data=json.dumps({
            'username': 'newuser',
            'password': 'W3lc0m3!2345',
            'repassword': 'W3lc0m3!2345',
            'first_name': 'First',
            'last_name': 'Last'
        }), content_type='application/json') 
        self.assertEqual(response.status_code, 200)  
        self.assertEqual(response.json()['message'], 'Successfully register.')
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_with_password_mismatch(self):
        # Simulate a POST request with password mismatch
        response = self.client.post(reverse('web:register_request'), data=json.dumps({
            'username': 'newuser',
            'password': 'password123',
            'repassword': 'password456',
            'first_name': 'First',
            'last_name': 'Last'
        }), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error']['repassword'], ['Passwords do not match.'])

    def test_register_with_weak_password(self):
        # Simulate a POST request with a weak password
        response = self.client.post(reverse('web:register_request'), data=json.dumps({
            'username': 'newuser',
            'password': '123',
            'repassword': '123',
            'first_name': 'First',
            'last_name': 'Last'
        }), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('password', response.json()['error'])

    def test_register_with_existing_username(self):
        # Create an existing user
        User.objects.create_user(username='existinguser', password='password123')

        # Simulate a POST request with an existing username
        response = self.client.post(reverse('web:register_request'), data=json.dumps({
            'username': 'existinguser',
            'password': 'W3lc0m3!2345',
            'repassword': 'W3lc0m3!2345',
            'first_name': 'First',
            'last_name': 'Last'
        }), content_type='application/json') 
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error']['username'][0], 'Username already exist!') 