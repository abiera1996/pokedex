from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Pokemon, Type, Ability
from .serializers import PokemonSerializer, PokemonDetailsSerializer

class PokemonViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password')
        
        # Obtain JWT token
        self.token = RefreshToken.for_user(self.user).access_token
        
        # Create test data for Type and Ability
        self.type1 = Type.objects.create(name='Electric')
        self.type2 = Type.objects.create(name='Fire')
        self.ability1 = Ability.objects.create(name='Static')
        self.ability2 = Ability.objects.create(name='Blaze')
        
        # Create test data for Pokemon
        self.pokemon1 = Pokemon.objects.create(
            name='Pikachu', 
            default_photo='http://example.com/pikachu.jpg', 
            height=0.4, 
            weight=6.0
        )
        self.pokemon1.types.add(self.type1)
        self.pokemon1.abilities.add(self.ability1)

        self.pokemon2 = Pokemon.objects.create(
            name='Charmander', 
            default_photo='http://example.com/charmander.jpg', 
            height=0.6, 
            weight=8.5
        )
        self.pokemon2.types.add(self.type2)
        self.pokemon2.abilities.add(self.ability2)

        self.valid_payload = {
            'name': 'Bulbasaur',
            'default_photo': 'http://example.com/bulbasaur.jpg',
            'types': [self.type1.id, self.type2.id],
            'abilities': [self.ability1.id, self.ability2.id],
            'height': 0.7,
            'weight': 6.9
        }
        self.invalid_payload = {
            'name': '',
            'default_photo': 'http://example.com/bulbasaur.jpg',
            'types': [self.type1.id, self.type2.id],
            'abilities': [self.ability1.id, self.ability2.id],
            'height': 0.7,
            'weight': 6.9
        }

    def test_get_pokemon_list(self):
        url = reverse('pokemon-list')
        response = self.client.get(url)
        pokemons = Pokemon.objects.all()
        serializer = PokemonSerializer(pokemons, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        self.assertEqual(response.data['data']['results'], serializer.data)

    def test_get_pokemon_detail(self):
        url = reverse('pokemon-detail', kwargs={'pk': self.pokemon1.pk})
        response = self.client.get(url)
        serializer = PokemonDetailsSerializer(self.pokemon1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data'], serializer.data)

    def test_create_pokemon(self):
        url = reverse('pokemon-list')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))
        response = self.client.post(url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_pokemon_invalid(self):
        url = reverse('pokemon-list')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))
        response = self.client.post(url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_pokemon(self):
        url = reverse('pokemon-detail', kwargs={'pk': self.pokemon1.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))
        response = self.client.patch(url, {'name': 'Raichu'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.pokemon1.refresh_from_db()
        self.assertEqual(self.pokemon1.name, 'Raichu')

    def test_delete_pokemon(self):
        url = reverse('pokemon-detail', kwargs={'pk': self.pokemon1.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Pokemon.objects.filter(pk=self.pokemon1.pk).exists())
