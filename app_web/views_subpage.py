from django.shortcuts import render, redirect
from django.contrib.auth import logout
from utils.decorators import (
    require_logged,
    require_not_logged
)
from app_pokemon.models import (
    Pokemon
)
from utils import helpers


@require_logged()
def subpage_pokemon_list(request):
    """
    List SUBPAGE
    :param request:
    :return:
    """
    context = dict()

    query_params = request.GET
    _page = query_params.get("page", 1)
    _limit = query_params.get("limit", 10)
    _search = query_params.get("search", "") 
    _sort = query_params.get("sort", "")  
    
    queryset = Pokemon.objects.all().order_by('name')
  
            
    if _sort != "":
        queryset = queryset.order_by(_sort)
    if _search != "":
        orm_lookups = ['name__icontains']
        queryset = helpers.search_result(queryset, _search, orm_lookups)  

    queryset = helpers.Paginator(queryset).paginate(
        page=_page, limit=_limit
    )

    context.update({
        "data_list": queryset
    })
    return render(request, "screens/user/_subpage/pokemon_list.html", context)
