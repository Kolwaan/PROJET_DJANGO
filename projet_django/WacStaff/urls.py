# FICHIER DE L'APPLICATION
# C'est lui qui connaît les vues concrètes

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # '' est vide car c'est la page d'accueil (racine de l'app)
]