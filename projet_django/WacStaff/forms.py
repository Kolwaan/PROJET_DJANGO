from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Restaurant, Fonction, Collaborateur, Affectation


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['nom', 'adresse', 'codePostal', 'ville']
        labels = {
            'nom': 'Nom',
            'adresse': 'Adresse',
            'codePostal': 'Code postal',
            'ville': 'Ville',
        }


class FonctionForm(forms.ModelForm):
    class Meta:
        model = Fonction
        fields = ['intitulePoste']
        labels = {'intitulePoste': 'Intitulé du poste'}


class CollaborateurForm(forms.ModelForm):
    class Meta:
        model = Collaborateur
        fields = ['nom', 'prenom', 'email', 'admin', 'password']
        labels = {
            'nom': 'Nom',
            'prenom': 'Prénom',
            'email': 'Email',
            'admin': 'Administrateur',
            'password': 'Mot de passe (optionnel)',
        }
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }


class AffectationForm(forms.ModelForm):
    class Meta:
        model = Affectation
        # debut est auto_now_add donc non éditable ; fin peut être renseignée pour clôturer
        fields = ['collaborateur', 'restaurant', 'poste', 'fin']
        labels = {
            'collaborateur': 'Collaborateur',
            'restaurant': 'Restaurant',
            'poste': 'Poste / Fonction',
            'fin': 'Date de fin (laisser vide si en cours)',
        }
        widgets = {
            'fin': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fin'].input_formats = ['%Y-%m-%dT%H:%M']
