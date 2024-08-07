from utils import helpers, serializers as class_serializer
from rest_framework import serializers  
from .models import (
    Pokemon, Type, Ability
)
from django.db.models import CharField, Value as V, Q, Sum 


class AbilitySerializer(class_serializer.ModelSerializer): 

    class Meta:
        model = Ability
        fields = '__all__'
         

class TypeSerializer(class_serializer.ModelSerializer): 

    class Meta:
        model = Type
        fields = '__all__'
         

class PokemonSerializer(class_serializer.ModelSerializer): 

    class Meta:
        model = Pokemon
        fields = '__all__'


class PokemonDetailsSerializer(class_serializer.ModelSerializer): 

    abilities = AbilitySerializer(many=True)
    types = TypeSerializer(many=True)

    class Meta:
        model = Pokemon
        fields = '__all__'
         