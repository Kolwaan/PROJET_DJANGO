from django.db import models


class Collaborateur(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    prenom = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    date1ereEmbauche = models.DateTimeField(auto_now_add=True)
    admin = models.BooleanField(default=False)
    password = models.CharField(max_length=200, blank=True, null=True)    
    
    def __str__(self):
        return self.nom



class Restaurant(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    adresse = models.CharField(max_length=300, unique=True)
    codePostal = models.CharField(max_length=50)
    ville = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nom



class Fonction(models.Model):
    intitulePoste = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.intitulePoste



class Affectation(models.Model):
    collaborateur = models.ForeignKey(Collaborateur, on_delete=models.PROTECT, related_name='affectations') # One-to-Many
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT, related_name='affectations')   # One-to-Many
    poste = models.ForeignKey(Fonction, on_delete=models.PROTECT, related_name='affectations')  # One-to-Many
    # Avec Django, related_name évite d'ajouter une relation dans les autres classes 
    debut = models.DateTimeField(auto_now_add=True) # auto_now_add remplit automatiquement avec la date du jour à la création
    fin = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.collaborateur} — {self.restaurant}"