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
