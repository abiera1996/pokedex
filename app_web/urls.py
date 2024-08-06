from django.urls import path, include 
from . import views, views_ajax
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
]

urlpatterns = urlpatterns + urlpatterns_ajax