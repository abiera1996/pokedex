from django.urls import path, include 
from . import views, views_ajax, views_subpage, views_modal
app_name = 'web'

urlpatterns = [
    path('', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout_account, name='logout'),
    path('pokemon', views.pokemon, name='pokemon'),
    path('pokemon/<str:id>', views.pokemon_details, name='pokemon_details'),
]   

urlpatterns_ajax = [
    path('ajax/pokemon-request', views_ajax.PokemonRequestView.as_view(), name='create_pokemon_request'),
    path('ajax/pokemon-request/<str:id>', views_ajax.PokemonRequestView.as_view(), name='update_or_delete_pokemon_request'),
    path('ajax/login-request', views_ajax.LoginRequestView.as_view(), name='login_request'),
    path('ajax/register-request', views_ajax.RegisterRequestView.as_view(), name='register_request'),
    path('ajax/search-ability', views_ajax.SearchAbilityView.as_view(), name='search_ability'),
    path('ajax/search-type', views_ajax.SearchTypeView.as_view(), name='search_type'),
]

urlpatterns_subpage = [
    path('subpage/subpage-pokemon-list', views_subpage.subpage_pokemon_list, name='subpage_pokemon_list'), 
]

urlpatterns_modal = [
    path('modal/create-pokemon', views_modal.modal_create_pokemon, name='modal_create_pokemon'),
    path('modal/update-pokemon/<str:id>', views_modal.modal_update_pokemon, name='modal_update_pokemon'),
]
urlpatterns = urlpatterns + urlpatterns_ajax + urlpatterns_subpage + urlpatterns_modal