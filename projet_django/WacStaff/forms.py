from django import forms
from django.contrib.auth import authenticate
from .models import Restaurant, Fonction, Collaborateur, Affectation


# ─────────────────────────────────────────────
# FORMULAIRE DE CONNEXION
# ─────────────────────────────────────────────

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'votre@email.fr'}))
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            self.user = authenticate(self.request, username=email, password=password)
            if self.user is None:
                raise forms.ValidationError("Email ou mot de passe incorrect.")
        return self.cleaned_data

    def get_user(self):
        return self.user


# ─────────────────────────────────────────────
# FORMULAIRE DE CRÉATION DE COLLABORATEUR
# Le champ "admin" n'est visible que pour les superusers
# ─────────────────────────────────────────────

class CollaborateurCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label='Confirmer le mot de passe',
        widget=forms.PasswordInput,
    )

    class Meta:
        model = Collaborateur
        fields = ['nom', 'prenom', 'email', 'admin']
        labels = {
            'nom': 'Nom',
            'prenom': 'Prénom',
            'email': 'Email',
            'admin': 'Administrateur',
        }

    def __init__(self, *args, superuser=False, **kwargs):
        super().__init__(*args, **kwargs)
        # Seul un superuser peut attribuer le statut admin à la création
        if not superuser:
            self.fields.pop('admin')

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned_data

    def save(self, commit=True):
        collaborateur = super().save(commit=False)
        collaborateur.set_password(self.cleaned_data['password1'])
        if commit:
            collaborateur.save()
        return collaborateur


# ─────────────────────────────────────────────
# FORMULAIRE DE MODIFICATION DE COLLABORATEUR
# Le champ "admin" n'est visible que pour les superusers
# ─────────────────────────────────────────────

class CollaborateurChangeForm(forms.ModelForm):
    class Meta:
        model = Collaborateur
        fields = ['nom', 'prenom', 'email', 'admin']
        labels = {
            'nom': 'Nom',
            'prenom': 'Prénom',
            'email': 'Email',
            'admin': 'Administrateur',
        }

    def __init__(self, *args, superuser=False, **kwargs):
        super().__init__(*args, **kwargs)
        # Seul un superuser peut modifier le statut admin
        if not superuser:
            self.fields.pop('admin')


# ─────────────────────────────────────────────
# AUTRES FORMULAIRES
# ─────────────────────────────────────────────

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


class AffectationForm(forms.ModelForm):
    class Meta:
        model = Affectation
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
