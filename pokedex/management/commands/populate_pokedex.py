import requests
from django.core.management.base import BaseCommand
from app_pokemon.models import (
    Pokemon, 
    Type, 
    Ability
)

class Command(BaseCommand):
    help = 'Fetch and store Pokémon data from the PokeAPI'

    def handle(self, *args, **kwargs):
        url = 'https://pokeapi.co/api/v2/pokemon?limit=151'
        response = requests.get(url)
        data = response.json()

        for item in data['results']:
            pokemon_data = requests.get(item['url']).json()
            
            types = []
            for type_info in pokemon_data['types']:
                type_name = type_info['type']['name']
                type_obj, created = Type.objects.get_or_create(name=type_name)
                types.append(type_obj)
            
            abilities = []
            for ability_info in pokemon_data['abilities']:
                ability_name = ability_info['ability']['name']
                ability_obj, created = Ability.objects.get_or_create(name=ability_name)
                abilities.append(ability_obj)

            pokemon, created = Pokemon.objects.get_or_create(
                name=pokemon_data['name'],
                photo=pokemon_data['sprites']['front_default'],
                height=pokemon_data['height'],
                weight=pokemon_data['weight']
            )
            pokemon.types.set(types)
            pokemon.abilities.set(abilities)
            pokemon.save()

        self.stdout.write(self.style.SUCCESS('Successfully fetched and stored Pokemon data'))
