from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from . import serializers
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.decorators import api_view, permission_classes as view_permission
from django.db.models.functions import Concat, Lower
from django.db.models import CharField, Value as V, Q
from datetime import datetime, timedelta, date
from .models import (
    Pokemon
) 
import csv
from django.http import HttpResponse   
import string
from django.db import transaction
import requests
from django.db.models.functions import Coalesce
from django.db.models import F, Count, IntegerField, Subquery, OuterRef, Case, When
from django.template.loader import get_template, render_to_string
from drf_spectacular.utils import (OpenApiResponse, extend_schema, OpenApiExample)
from . import response_serializer
from utils import helpers 
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.types import OpenApiTypes


@extend_schema( 
    tags=['Pokemon']
)
class PokemonView(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete'] 
    queryset = Pokemon.objects.all()
    serializer_class = serializers.PokemonSerializer 
    action_serializers = {
        'retrieve': serializers.PokemonDetailsSerializer 
    }

    def get_serializer_class(self):
        """
        Retrieve the appropriate serializer for every request method
        """
        if hasattr(self, "action_serializers"):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]

        return super().get_serializer_class() 
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """ 
        if self.action in ('list', 'retrieve'):
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]  # Default permission

        return [permission() for permission in permission_classes]
    
    @extend_schema(   
        auth=[],
        parameters=list([ 
            OpenApiParameter(
                name="search", location=OpenApiParameter.QUERY, type=OpenApiTypes.STR, required=False, default=""),
            OpenApiParameter(
                name="paginate", location=OpenApiParameter.QUERY, type=OpenApiTypes.BOOL, required=False, default=True)
        ]),
        summary='List of Pokemon',
        responses={
            200: response_serializer.PokemonListResponseSerializer
        }
    )
    def list(self, request, *args, **kwargs):
        """
        Get the list of pokemon.
        """
        data = request.GET
        queryset = self.filter_queryset(self.get_queryset())   
        if data.get('search', '') != '':
            orm_lookups = ['name__icontains']
            queryset = helpers.search_result(queryset, data.get('search'), orm_lookups)  

        if data.get('paginate', 'true') == 'true':
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
   
    @extend_schema(  
        auth=[],  
        summary='Get Pokemon Details',
        responses={
            200: response_serializer.PokemonDetailsResponseSerializer, 
            404: response_serializer.PokemonDetailsNotFoundResponseSerializer
        }
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Get pokemon details.
        """
        instance=self.get_object()

        # Read event notification
        serializer=self.get_serializer(instance)
        return Response(serializer.data)

    @extend_schema(   
        summary='Create Pokemon',
        responses={ 
            201: response_serializer.PokemonCreateReponseSerializer,
            400: response_serializer.ErrorFieldSerializer,
            401: response_serializer.AuthenticationErrorSerializer
        }
    )
    def create(self, request, *args, **kwargs):
        """
        Add new Pokemon.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Pokemon successfully added.'
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.get_error_response(), status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(   
        summary='Update Pokemon',
        responses={
            200: response_serializer.PokemonUpdateReponseSerializer,
            400: response_serializer.ErrorFieldSerializer,
            401: response_serializer.AuthenticationErrorSerializer,
            404: response_serializer.PokemonDetailsNotFoundResponseSerializer
        }
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Update pokemon details
        """
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Pokemon successfully updated.'
            }, status=status.HTTP_200_OK)

        return Response(serializer.get_error_response(), status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(   
        summary='Delete Pokemon',
        responses={
            200: response_serializer.PokemonDeleteReponseSerializer,
            401: response_serializer.AuthenticationErrorSerializer,
            404: response_serializer.PokemonDetailsNotFoundResponseSerializer
        }
    )
    def destroy(self, request, *args, **kwargs):
        """
        Delete specific Pokemon
        """
        instance = self.get_object() 

        self.perform_destroy(instance)
        return Response({
            'message': 'Pokemon successfully deleted.'
        }, status=status.HTTP_200_OK)