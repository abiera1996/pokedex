from django.urls import path, include 
from . import views, views_ajax, views_subpage
app_name = 'web'

urlpatterns = [
    path('', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout_account, name='logout'),
    path('pokemon', views.pokemon, name='pokemon'),
    path('pokemon/<str:id>', views.pokemon_details, name='pokemon_details'),
]   

urlpatterns_ajax = [
    path('ajax/login-request', views_ajax.login_request, name='login_request'),
    path('ajax/register-request', views_ajax.register_request, name='register_request'),
    path('ajax/create-pokemon-request', views_ajax.create_pokemon_request, name='create_pokemon_request'), 
    path('ajax/update-pokemon-request/<str:id>', views_ajax.update_pokemon_request, name='update_pokemon_request'),
    path('ajax/delete-pokemon-request/<str:id>', views_ajax.delete_pokemon_request, name='delete_pokemon_request'),
]

urlpatterns_subpage = [
    path('subpage/subpage-pokemon-list', views_subpage.subpage_pokemon_list, name='subpage_pokemon_list'), 
]

urlpatterns = urlpatterns + urlpatterns_ajax + urlpatterns_subpage