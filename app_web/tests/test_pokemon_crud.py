from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from app_pokemon.models import Pokemon, Type, Ability  
import json
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile


class PokemonRequestTestCase(TestCase):
    def setUp(self):
        # Create a user and log in
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client = Client()
        self.client.login(username='testuser', password='password')
        
        # Create some types and abilities
        self.type1 = Type.objects.create(name='Type1')
        self.type2 = Type.objects.create(name='Type2')
        self.ability1 = Ability.objects.create(name='Ability1')
        self.ability2 = Ability.objects.create(name='Ability2')

    def test_create_pokemon_request(self):
        url = reverse('web:create_pokemon_request')
        data = {
            'name': 'Pikachu',
            'height': 1.2,
            'weight': 30.0,
            'types': [self.type1.pk, self.type2.pk],
            'abilities': [self.ability1.pk, self.ability2.pk]
        }
        photo = SimpleUploadedFile("photo.jpg", b"file_content", content_type="image/jpeg")
        response = self.client.post(url, data, format='multipart', **{'photo': photo})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Successfully created.')
        self.assertTrue(Pokemon.objects.filter(name='Pikachu').exists())

    def test_create_pokemon_with_existing_name(self):
        Pokemon.objects.create(name='Pikachu', height=1.0, weight=20.0)
        url = reverse('web:create_pokemon_request')
        data = {
            'name': 'Pikachu',
            'height': 1.2,
            'weight': 30.0
        }
        response = self.client.post(url, data, format='multipart')
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error']['name'], 'Pokemon name already exist!')

    def test_update_pokemon_request(self):
        pokemon = Pokemon.objects.create(name='Bulbasaur', height=1.0, weight=20.0)
        url = reverse('web:update_pokemon_request', args=[pokemon.pk])
        data = {
            'name': 'Ivysaur',
            'height': 1.5,
            'weight': 25.0,
            'types': self.type1.pk,
            'abilities': self.ability1.pk
        }
        photo = SimpleUploadedFile("photo.jpg", b"file_content", content_type="image/jpeg") 
        response = self.client.post(url, json.dumps(data), format='multipart', content_type='application/json', **{'photo': photo})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Successfully updated.')
        updated_pokemon = Pokemon.objects.get(pk=pokemon.pk)
        self.assertEqual(updated_pokemon.name, 'Ivysaur')
        self.assertEqual(updated_pokemon.height, 1.5)
        self.assertEqual(updated_pokemon.weight, 25.0)

    def test_update_pokemon_with_existing_name(self):
        Pokemon.objects.create(name='Charmander', height=1.0, weight=20.0)
        pokemon = Pokemon.objects.create(name='Bulbasaur', height=1.0, weight=20.0)
        url = reverse('web:update_pokemon_request', args=[pokemon.pk])
        data = {
            'name': 'Charmander',
            'height': 1.5,
            'weight': 25.0
        }
        response = self.client.post(url, json.dumps(data), format='multipart', content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error']['name'], 'Pokemon name already exist!')

    def test_delete_pokemon_request(self):
        pokemon = Pokemon.objects.create(name='Squirtle', height=1.0, weight=20.0)
        url = reverse('web:delete_pokemon_request', args=[pokemon.pk])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Successfully Deleted.')
        self.assertFalse(Pokemon.objects.filter(pk=pokemon.pk).exists())

    def test_delete_nonexistent_pokemon(self):
        url = reverse('web:delete_pokemon_request', args=[999])  # Assuming 999 does not exist
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['message'], 'Pokemon id not found.')
