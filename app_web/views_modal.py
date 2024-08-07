from django.shortcuts import render, reverse, redirect 
from app_pokemon.models import Pokemon
from django.shortcuts import get_object_or_404

def modal_create_pokemon(request):  
    data = dict(zip(request.GET.keys(), request.GET.values()))
    
    context = {}
    return render(request, template_name='screens/user/_modals/create_pokemon.html', context=context)


def modal_update_pokemon(request, id):  
    data = dict(zip(request.GET.keys(), request.GET.values()))
    details = get_object_or_404(Pokemon, pk=id)
    context = {
        'id': id,
        'details': details
    }
    return render(request, template_name='screens/user/_modals/create_pokemon.html', context=context)