# À chaque modif d'un modèle, on doit faire une migration.

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# ─────────────────────────────────────────────
# MANAGER PERSONNALISÉ POUR COLLABORATEUR
# Nécessaire quand on remplace le modèle User par défaut.
# Django l'utilise pour créer des utilisateurs via create_user() et create_superuser().
# ─────────────────────────────────────────────

class CollaborateurManager(BaseUserManager):
    def create_user(self, email, nom, prenom, password=None):
        if not email:
            raise ValueError("L'email est obligatoire")
        user = self.model(
            email=self.normalize_email(email),  # normalise l'email (minuscules sur le domaine)
            nom=nom,
            prenom=prenom,
        )
        user.set_password(password)  # hash automatique du mot de passe
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nom, prenom, password):
        user = self.create_user(email, nom, prenom, password)
        user.admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# ─────────────────────────────────────────────
# COLLABORATEUR — remplace le modèle User de Django
# ─────────────────────────────────────────────

# Collaborateur est le user, il le remplace complètement.
# C'est la table en BDD
class Collaborateur(AbstractBaseUser, PermissionsMixin):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    date1ereEmbauche = models.DateTimeField(auto_now_add=True)
    admin = models.BooleanField(default=False)
    # NB : le champ password est déjà géré par AbstractBaseUser

    USERNAME_FIELD = 'email'            # champ utilisé pour se connecter
    REQUIRED_FIELDS = ['nom', 'prenom'] # champs demandés par createsuperuser en plus de l'email

    objects = CollaborateurManager()

    @property
    def is_staff(self):
        # Django consulte is_staff pour l'accès à /admin/ et aux vues
        # On le branche directement sur le champ admin
        return self.admin

    def __str__(self):
        return f"{self.prenom} {self.nom}"


# ─────────────────────────────────────────────
# RESTAURANT
# ─────────────────────────────────────────────

class Restaurant(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    adresse = models.CharField(max_length=300, unique=True)
    codePostal = models.CharField(max_length=50)
    ville = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


# ─────────────────────────────────────────────
# FONCTION
# ─────────────────────────────────────────────

class Fonction(models.Model):
    intitulePoste = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.intitulePoste


# ─────────────────────────────────────────────
# AFFECTATION
# ─────────────────────────────────────────────

class Affectation(models.Model):
    collaborateur = models.ForeignKey(Collaborateur, on_delete=models.PROTECT, related_name='affectations')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT, related_name='affectations')
    poste = models.ForeignKey(Fonction, on_delete=models.PROTECT, related_name='affectations')
    debut = models.DateTimeField(auto_now_add=True)
    fin = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.collaborateur} — {self.restaurant}"
