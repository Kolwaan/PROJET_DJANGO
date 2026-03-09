# DÉCIDE QUOI AFFICHER

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm


# VUE D'ACCUEIL
@login_required      # pour ne pas que ce soit accessible à tout le monde
def home(request):                  # La fonction home est une vue. Elle reçoit une requête HTTP (ici GET)
                                    # et renvoie une réponse.
                                        
    return render(request, "home.html") # va chercher le HTML et le retourne
                                        # request : la requête du navigateur
                                        # home.html : le template



# VUE POUR L'INSCRIPTION
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # home : vue d'accueil
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


# VUE POUR LA CONNEXION
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


# VUE POUR LA DÉCONNEXION
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirige vers la page de connexion après la déconnexion

