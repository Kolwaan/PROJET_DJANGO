from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User  # Utilise le modèle utilisateur par défaut
        fields = ('username', 'email', 'password1', 'password2')