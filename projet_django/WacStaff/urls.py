# FICHIER DE L'APPLICATION
# C'est lui qui connaît les vues concrètes

from django.urls import path
from . import views
from .views import register_view, login_view, logout_view

urlpatterns = [
    path('', views.home, name='home'),  # '' est vide car c'est la page d'accueil (racine de l'app)
    
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout')
]