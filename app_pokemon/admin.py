from django.contrib import admin
from .models import (
    Pokemon,
    Type,
    Ability
) 

    
@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):  
    list_display = ('name', 'height', 'weight') 
    search_fields = ("name",)  

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):  
    list_display = ('name', ) 
    search_fields = ("name",) 


@admin.register(Ability)
class AbilityAdmin(admin.ModelAdmin):  
    list_display = ('name', ) 
    search_fields = ("name",) 