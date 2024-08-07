from django.urls import path, include 
from rest_framework import routers
from .views import PokemonView


pokemon_routers  = routers.DefaultRouter()
pokemon_routers.register('', PokemonView, basename='pokemon')

urlpatterns = [ 
    path('pokemon/', include(pokemon_routers.urls)), 
] 