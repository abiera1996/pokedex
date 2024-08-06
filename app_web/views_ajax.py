from django.shortcuts import render, reverse, redirect
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse
import datetime, json 
from django.contrib.auth.models import User
from utils.helpers import (
    decode_request_body, 
)
from django.db import transaction
from django.contrib.auth import password_validation, authenticate, login
from django.core.exceptions import ValidationError
from django.db.models import F, Value, CharField, Subquery, OuterRef, Case, When, IntegerField, DateField, \
    FloatField
from django.db.models.functions import Coalesce
from django.db.models import Q, OuterRef
from threading import Thread
from django.template.loader import get_template
from utils import helpers
from utils.decorators import (
    require_logged,
    require_not_logged
)
from app_pokemon.models import (
    Pokemon,
    Type,
    Ability
)

@require_http_methods(['POST'])
def login_request(request):
    try:
        data = decode_request_body(request.body)
    except Exception as e:
        data = request.POST 
    username = data.get('username', '')
    password = data.get('password', '')
    user = User.objects.filter(email=username)
    if user.exists():
        username = user[0].username
    
    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({
            'message': 'Username\Email or password is incorrect.'
        }, status=400)
    
    login(request, user)
   
    return JsonResponse({
        'message': 'Successfully login.'
    }, status=200)

 
@require_http_methods(['POST'])
def register_request(request):
    try:
        data = decode_request_body(request.body)
    except Exception as e:
        data = request.POST
    
    errors = {}  
    if data['password'] != data['repassword']:
        return JsonResponse({
            'error': {
                "repassword": ['Passwords do not match.' ]
            }
        }, status=400)
    try:
        if data.get('password'):
            password_validation.validate_password(data['password'])
        
    except ValidationError as e: 
        errors['password'] = e.messages
        
    if not errors:
        user = User.objects.filter( username=data['username'])
        if user.exists():
            errors['username'] = 'Username already exist!'
             
    if errors:
        return JsonResponse({ 
            "error": errors
        }, status=400) 

    with transaction.atomic():
        password = data.get('password', '') 
 
        if password == '' or password is None:
            password = User.objects.make_random_password(8) 
            
        user = User.objects.create_user(
            username=data['username'],
            password=password, 
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', '')
        )
    return JsonResponse({
        'message': 'Successfully register.'
    }, status=200)



@require_logged()
@require_http_methods(['POST'])
def create_pokemon_request(request):
    try:
        data = decode_request_body(request.body)
    except Exception as e:
        data = request.POST
    files = request.FILES

    errors = {} 
    if data.get('name', ''):  
        is_existing = Pokemon.objects.filter( 
            name=data['name']
        ).exists()
        if is_existing:
            errors['name'] = 'Pokemon name already exist!'
            
    if errors:
        return JsonResponse({ 
            "error": errors
        }, status=400) 

    with transaction.atomic():
        pokemon = Pokemon()
        pokemon.name = data.get('name', '')
        pokemon.height = data.get('height', 0)
        pokemon.weight = data.get('weight', 0)  
        pokemon.save()

        if data.get('types'):
            types = Type.objects.filter(
                pk__in=data.getlist('types',[])
            ) 
            pokemon.types.add(*types)
            pokemon.save()
            
        if data.get('abilities'):
            abilities = Ability.objects.filter(
                pk__in=data.getlist('abilities',[])
            ) 
            pokemon.abilities.add(*abilities)
            pokemon.save()

        if files.get('photo'):
            pokemon.photo = files.get('photo').open()
            pokemon.save()

    return JsonResponse({
        'message': 'Successfully created.'
    }, status=200)


@require_logged()
@require_http_methods(['PATCH'])
def update_pokemon_request(request, id):
    try:
        data = decode_request_body(request.body)
    except Exception as e:
        data = request.PATCH
    files = request.FILES

    pokemon = helpers.get_or_none(Pokemon, pk=id) 
    if pokemon is None:
        return JsonResponse({
            'message': 'Pokemon id not found.'
        }, status=404)
    
    errors = {} 
    if data.get('name', ''):  
        is_existing = Pokemon.objects.filter( 
            name=data['name']
        ).exclude(pk=id).exists()
        if is_existing:
            errors['name'] = 'Pokemon name already exist!'
            
    if errors:
        return JsonResponse({ 
            "error": errors
        }, status=400) 

    with transaction.atomic():
        pokemon.name = data.get('name', pokemon.name)
        pokemon.height = data.get('height', pokemon.height)
        pokemon.weight = data.get('weight', pokemon.weight)  
        pokemon.save()

        if files.get('photo'):
            pokemon.photo = files.get('photo').open()
            pokemon.save() 
        if data.get('types'):
            types = Type.objects.filter(
                pk__in=data.get('types',[])
            )
            pokemon.types.clear()
            pokemon.types.add(*types)
            pokemon.save()
            
        if data.get('abilities'):
            abilities = Ability.objects.filter(
                pk__in=data.get('abilities',[])
            )
            pokemon.abilities.clear()
            pokemon.abilities.add(*abilities)
            pokemon.save()

    return JsonResponse({
        'message': 'Successfully updated.'
    }, status=200)


@require_logged()
@require_http_methods(['DELETE'])
def delete_pokemon_request(request, id): 
    pokemon = helpers.get_or_none(Pokemon, pk=id) 
    if pokemon is None:
        return JsonResponse({
            'message': 'Pokemon id not found.'
        }, status=404)
    pokemon.delete()
    return JsonResponse({
        'message': 'Successfully Deleted.'
    }, status=200)