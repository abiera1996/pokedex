from django.urls import path, include 
from . import views
app_name = 'web'

urlpatterns = [
    path('', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout_account, name='logout'),
    path('pokemon', views.pokemon, name='pokemon'),
    path('pokemon/<str:id>', views.pokemon_details, name='pokemon_details'),
]  