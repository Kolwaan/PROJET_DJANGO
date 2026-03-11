# DÉCIDE QUOI AFFICHER

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import (
    CustomUserCreationForm,
    RestaurantForm, FonctionForm, CollaborateurForm, AffectationForm
)
from .models import Restaurant, Fonction, Collaborateur, Affectation


# ─────────────────────────────────────────────
# ACCUEIL
# ─────────────────────────────────────────────

@login_required
def home(request):
    return render(request, "home.html", {
        'nb_restaurants': Restaurant.objects.count(),
        'nb_collaborateurs': Collaborateur.objects.count(),
        'nb_fonctions': Fonction.objects.count(),
        'nb_affectations': Affectation.objects.count(),
    })


# ─────────────────────────────────────────────
# AUTH
# ─────────────────────────────────────────────

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


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


def logout_view(request):
    logout(request)
    return redirect('login')


# ─────────────────────────────────────────────
# RESTAURANTS
# ─────────────────────────────────────────────

@login_required
def restaurant_list(request):
    qs = Restaurant.objects.all()
    q_nom = request.GET.get('nom', '')
    q_cp = request.GET.get('codePostal', '')
    q_ville = request.GET.get('ville', '')
    if q_nom:
        qs = qs.filter(nom__icontains=q_nom)
    if q_cp:
        qs = qs.filter(codePostal__icontains=q_cp)
    if q_ville:
        qs = qs.filter(ville__icontains=q_ville)
    return render(request, 'restaurants/list.html', {
        'restaurants': qs, 'q_nom': q_nom, 'q_cp': q_cp, 'q_ville': q_ville,
    })


@login_required
def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    affectations = restaurant.affectations.select_related('collaborateur', 'poste')
    q_poste = request.GET.get('poste', '')
    q_debut = request.GET.get('debut', '')
    if q_poste:
        affectations = affectations.filter(poste__intitulePoste__icontains=q_poste)
    if q_debut:
        affectations = affectations.filter(debut__date__gte=q_debut)
    return render(request, 'restaurants/detail.html', {
        'restaurant': restaurant, 'affectations': affectations,
        'fonctions': Fonction.objects.all(), 'q_poste': q_poste, 'q_debut': q_debut,
    })


@login_required
def restaurant_create(request):
    if not request.user.is_staff:
        messages.error(request, "Accès réservé aux administrateurs.")   # notification flash
        return redirect('restaurant_list')
    form = RestaurantForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Restaurant créé avec succès.")   # notification flash
        return redirect('restaurant_list')
    return render(request, 'restaurants/form.html', {'form': form, 'action': 'Créer'})


@login_required
def restaurant_edit(request, pk):
    if not request.user.is_staff:
        messages.error(request, "Accès réservé aux administrateurs.")
        return redirect('restaurant_list')
    restaurant = get_object_or_404(Restaurant, pk=pk)
    form = RestaurantForm(request.POST or None, instance=restaurant)
    if form.is_valid():
        form.save()
        messages.success(request, "Restaurant modifié.")
        return redirect('restaurant_detail', pk=pk)
    return render(request, 'restaurants/form.html', {
        'form': form, 'action': 'Modifier', 'obj': restaurant
    })


# ─────────────────────────────────────────────
# FONCTIONS
# ─────────────────────────────────────────────

@login_required
def fonction_list(request):
    return render(request, 'fonctions/list.html', {'fonctions': Fonction.objects.all()})


@login_required
def fonction_create(request):
    if not request.user.is_staff:
        messages.error(request, "Accès réservé aux administrateurs.")
        return redirect('fonction_list')
    form = FonctionForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Fonction créée.")
        return redirect('fonction_list')
    return render(request, 'fonctions/form.html', {'form': form, 'action': 'Créer'})


@login_required
def fonction_edit(request, pk):
    if not request.user.is_staff:
        messages.error(request, "Accès réservé aux administrateurs.")
        return redirect('fonction_list')
    fonction = get_object_or_404(Fonction, pk=pk)
    form = FonctionForm(request.POST or None, instance=fonction)
    if form.is_valid():
        form.save()
        messages.success(request, "Fonction modifiée.")
        return redirect('fonction_list')
    return render(request, 'fonctions/form.html', {
        'form': form, 'action': 'Modifier', 'obj': fonction
    })


@login_required
def fonction_delete(request, pk):
    if not request.user.is_staff:
        messages.error(request, "Accès réservé aux administrateurs.")
        return redirect('fonction_list')
    fonction = get_object_or_404(Fonction, pk=pk)
    if request.method == 'POST':
        try:
            fonction.delete()
            messages.success(request, "Fonction supprimée.")
        except Exception:
            messages.error(request, "Impossible : des affectations utilisent cette fonction.")
    return redirect('fonction_list')


# ─────────────────────────────────────────────
# COLLABORATEURS
# ─────────────────────────────────────────────

@login_required
def collaborateur_list(request):
    qs = Collaborateur.objects.all()
    q_nom = request.GET.get('nom', '')
    q_prenom = request.GET.get('prenom', '')
    q_email = request.GET.get('email', '')
    non_affectes = request.GET.get('non_affectes', '')
    if q_nom:
        qs = qs.filter(nom__icontains=q_nom)
    if q_prenom:
        qs = qs.filter(prenom__icontains=q_prenom)
    if q_email:
        qs = qs.filter(email__icontains=q_email)
    if non_affectes:
        # Collaborateurs sans aucune affectation active (fin est null)
        active_ids = Affectation.objects.filter(fin__isnull=True).values('collaborateur_id')
        qs = qs.exclude(pk__in=active_ids)
    return render(request, 'collaborateurs/list.html', {
        'collaborateurs': qs, 'q_nom': q_nom, 'q_prenom': q_prenom,
        'q_email': q_email, 'non_affectes': non_affectes,
    })


@login_required
def collaborateur_detail(request, pk):
    collaborateur = get_object_or_404(Collaborateur, pk=pk)
    affectations = collaborateur.affectations.select_related('restaurant', 'poste')
    q_poste = request.GET.get('poste', '')
    q_debut = request.GET.get('debut', '')
    if q_poste:
        affectations = affectations.filter(poste__intitulePoste__icontains=q_poste)
    if q_debut:
        affectations = affectations.filter(debut__date__gte=q_debut)
    return render(request, 'collaborateurs/detail.html', {
        'collaborateur': collaborateur,
        'affectations_actives': affectations.filter(fin__isnull=True),
        'affectations_historique': affectations.filter(fin__isnull=False),
        'q_poste': q_poste, 'q_debut': q_debut,
    })


@login_required
def collaborateur_create(request):
    if not request.user.is_staff:
        messages.error(request, "Accès réservé aux administrateurs.")
        return redirect('collaborateur_list')
    form = CollaborateurForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Collaborateur créé.")
        return redirect('collaborateur_list')
    return render(request, 'collaborateurs/form.html', {'form': form, 'action': 'Créer'})


@login_required
def collaborateur_edit(request, pk):
    if not request.user.is_staff:
        messages.error(request, "Accès réservé aux administrateurs.")
        return redirect('collaborateur_list')
    collaborateur = get_object_or_404(Collaborateur, pk=pk)
    form = CollaborateurForm(request.POST or None, instance=collaborateur)
    if form.is_valid():
        form.save()
        messages.success(request, "Collaborateur modifié.")
        return redirect('collaborateur_detail', pk=pk)
    return render(request, 'collaborateurs/form.html', {
        'form': form, 'action': 'Modifier', 'obj': collaborateur
    })


# ─────────────────────────────────────────────
# AFFECTATIONS
# ─────────────────────────────────────────────

@login_required
def affectation_list(request):
    qs = Affectation.objects.select_related('collaborateur', 'restaurant', 'poste')
    q_poste = request.GET.get('poste', '')
    q_debut = request.GET.get('debut', '')
    q_fin = request.GET.get('fin', '')
    q_ville = request.GET.get('ville', '')
    if q_poste:
        qs = qs.filter(poste__intitulePoste__icontains=q_poste)
    if q_debut:
        qs = qs.filter(debut__date__gte=q_debut)
    if q_fin:
        qs = qs.filter(fin__date__lte=q_fin)
    if q_ville:
        qs = qs.filter(restaurant__ville__icontains=q_ville)
    return render(request, 'affectations/list.html', {
        'affectations': qs, 'q_poste': q_poste, 'q_debut': q_debut,
        'q_fin': q_fin, 'q_ville': q_ville,
    })


@login_required
def affectation_create(request):
    if not request.user.is_staff:
        messages.error(request, "Accès réservé aux administrateurs.")
        return redirect('affectation_list')
    initial = {}
    if request.GET.get('collaborateur'):
        initial['collaborateur'] = request.GET['collaborateur']
    if request.GET.get('restaurant'):
        initial['restaurant'] = request.GET['restaurant']
    form = AffectationForm(request.POST or None, initial=initial)
    if form.is_valid():
        form.save()
        messages.success(request, "Affectation créée.")
        return redirect('affectation_list')
    return render(request, 'affectations/form.html', {'form': form, 'action': 'Créer'})


@login_required
def affectation_edit(request, pk):
    if not request.user.is_staff:
        messages.error(request, "Accès réservé aux administrateurs.")
        return redirect('affectation_list')
    affectation = get_object_or_404(Affectation, pk=pk)
    form = AffectationForm(request.POST or None, instance=affectation)
    if form.is_valid():
        form.save()
        messages.success(request, "Affectation modifiée.")
        return redirect('affectation_list')
    return render(request, 'affectations/form.html', {
        'form': form, 'action': 'Modifier', 'obj': affectation
    })


@login_required
def affectation_delete(request, pk):
    if not request.user.is_staff:
        messages.error(request, "Accès réservé aux administrateurs.")
        return redirect('affectation_list')
    affectation = get_object_or_404(Affectation, pk=pk)
    if request.method == 'POST':
        affectation.delete()
        messages.success(request, "Affectation supprimée.")
    return redirect('affectation_list')
