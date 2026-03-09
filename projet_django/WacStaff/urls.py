# FICHIER DE L'APPLICATION

from django.urls import path
from . import views

urlpatterns = [
    # Accueil
    path('', views.home, name='home'),

    # Auth
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Restaurants
    path('restaurants/', views.restaurant_list, name='restaurant_list'),
    path('restaurants/nouveau/', views.restaurant_create, name='restaurant_create'),
    path('restaurants/<int:pk>/', views.restaurant_detail, name='restaurant_detail'),
    path('restaurants/<int:pk>/modifier/', views.restaurant_edit, name='restaurant_edit'),

    # Fonctions
    path('fonctions/', views.fonction_list, name='fonction_list'),
    path('fonctions/nouveau/', views.fonction_create, name='fonction_create'),
    path('fonctions/<int:pk>/modifier/', views.fonction_edit, name='fonction_edit'),
    path('fonctions/<int:pk>/supprimer/', views.fonction_delete, name='fonction_delete'),

    # Collaborateurs
    path('collaborateurs/', views.collaborateur_list, name='collaborateur_list'),
    path('collaborateurs/nouveau/', views.collaborateur_create, name='collaborateur_create'),
    path('collaborateurs/<int:pk>/', views.collaborateur_detail, name='collaborateur_detail'),
    path('collaborateurs/<int:pk>/modifier/', views.collaborateur_edit, name='collaborateur_edit'),

    # Affectations
    path('affectations/', views.affectation_list, name='affectation_list'),
    path('affectations/nouveau/', views.affectation_create, name='affectation_create'),
    path('affectations/<int:pk>/modifier/', views.affectation_edit, name='affectation_edit'),
    path('affectations/<int:pk>/supprimer/', views.affectation_delete, name='affectation_delete'),
]
