from django.shortcuts import render, redirect
from django.contrib.auth import logout
from utils.decorators import (
    require_logged,
    require_not_logged
)
from app_pokemon.models import Pokemon
from django.shortcuts import get_object_or_404


@require_not_logged
def login(request):  
    context = {
        'title': 'Pokedex - Login',
    } 
    return render(request, template_name='screens/auth/login.html', context=context)


@require_not_logged
def register(request):  
    context = {
        'title': 'Pokedex - Registration',
    } 
    return render(request, template_name='screens/auth/register.html', context=context)


@require_logged()
def pokemon(request):  
    context = {
        'title': 'Pokedex',
    } 
    return render(request, template_name='screens/user/pokemon.html', context=context)


@require_logged()
def pokemon_details(request, id):  
    details = get_object_or_404(Pokemon, pk=id)
    context = {
        'title': 'Pokedex',
        'id': id,
        'details': details
    } 
    return render(request, template_name='screens/user/pokemon_details.html', context=context)


def logout_account(request): 
    logout(request) 
    return redirect('web:login')